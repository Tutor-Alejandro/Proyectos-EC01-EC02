"""
interaction_cli.py
Interacción por consola (UX amigable, sin tablas ni índices):
- Ingresar FB-ID si el usuario lo tiene.
- Si no tiene FB-ID: modo guiado (elige categoría y nivel de atención aproximado).
- Cálculo del Focus Score y reporte amigable.
- Ingreso manual con recomendaciones y registro de bloques.
- Log de sesiones en CSV.
"""

from typing import Dict, Optional, Tuple, List
from datetime import datetime
import pandas as pd
from utils import normalize_string, bubble_sort
from focus_model import FocusScore, threshold_closure
from recommendations import recommend, classify_usage_hours
from time_tracking import track_blocks


# ---------- Helpers internos ----------

def _notifications_from_handling_text(text: Optional[str]) -> float:
    if text is None:
        return 30.0
    v = normalize_string(text)
    if "mute" in v or "silenc" in v:
        return 10.0
    if "manage" in v or "smart" in v or "resumen" in v:
        return 20.0
    if "frequent" in v or "many" in v or "muchas" in v or "alta" in v:
        return 60.0
    return 30.0


def _append_log(path: str, row_dict: Dict) -> None:
    df = pd.DataFrame([row_dict])
    df.to_csv(path, mode="a", index=False, header=not _file_exists(path))


def _file_exists(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8"):
            return True
    except FileNotFoundError:
        return False


def _friendly_report(score: float, attention: float, social_time: float, notifications: float) -> None:
    """Resumen en lenguaje natural (sin datos técnicos innecesarios)."""
    level = "BUENO" if score >= 70 else ("REGULAR" if score >= 50 else "BAJO")
    usage_label = classify_usage_hours(social_time)

    print(f"\nTu Focus Score: {score:.1f}  → Nivel: {level}")
    parts = []
    parts.append(f"atención {'alta' if attention>=70 else ('media' if attention>=40 else 'baja')} ({int(attention)}/100)")
    parts.append(f"uso {usage_label} (~{social_time:.1f} h)")
    parts.append(f"notificaciones {'altas' if notifications>=60 else ('medias' if notifications>=30 else 'bajas')} (~{int(notifications)})")
    print("Resumen:", ", ".join(parts) + ".")


# ---------- Asignación y búsqueda por FB-ID ----------

def _ensure_fb_id(df: pd.DataFrame) -> pd.DataFrame:
    """Crea una columna FB-ID estable (1001, 1002, ...) basada en el índice actual."""
    if "fb_id" not in df.columns:
        df = df.copy()
        df["fb_id"] = (df.index.astype(int) + 1001).astype(int)
    return df


def _find_index_by_fbid(df: pd.DataFrame, fbid_str: str) -> Optional[int]:
    try:
        fbid = int(fbid_str)
    except:
        return None
    hit = df.index[df["fb_id"] == fbid]
    if len(hit) == 1:
        return int(hit[0])
    return None


# ---------- Modo guiado (sin FB-ID) ----------

def _choose_from_list(prompt: str, options: List[str]) -> Optional[str]:
    """Pequeño menú enumerado 1..N para elegir una opción textual."""
    if not options:
        return None
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"[{i}] {opt}")
    while True:
        raw = input("Elige una opción: ").strip()
        if raw.isdigit():
            k = int(raw)
            if 1 <= k <= len(options):
                return options[k-1]
        print("Opción inválida. Intenta de nuevo.")


def _bucket_attention(att_num: Optional[float]) -> str:
    """Convierte atención numérica a etiquetas simples para el usuario."""
    if att_num is None:
        return "desconocido"
    try:
        v = float(att_num)
    except:
        return "desconocido"
    if v < 40:
        return "baja (0–39)"
    if v < 70:
        return "media (40–69)"
    return "alta (70–100)"


def _bucket_to_mid(att_bucket: str) -> float:
    """Representante numérico aproximado por bucket (para desempates)."""
    if att_bucket.startswith("baja"):
        return 20.0
    if att_bucket.startswith("media"):
        return 55.0
    if att_bucket.startswith("alta"):
        return 85.0
    return 55.0


def _guided_pick_index(df: pd.DataFrame) -> Optional[int]:
    """
    Modo guiado:
    1) Elegir categoría principal (derivada de app_category).
    2) Elegir nivel de atención aproximado (baja/media/alta).
    3) Si hay varias coincidencias, mostrar hasta 3 alternativas con sus FB-ID.
    """
    # 1) Categorías más comunes
    cat_col = "app_category" if "app_category" in df.columns else None
    if cat_col:
        cats = df[cat_col].astype(str).apply(lambda s: s.split("(")[0].strip()).tolist()
        top_cats = pd.Series(cats).value_counts().head(6).index.tolist()
        user_cat = _choose_from_list("Elige tu categoría principal (la que más usaste hoy):", top_cats)
    else:
        user_cat = None

    # 2) Atención aproximada
    att_bucket = _choose_from_list("Elige tu nivel de atención aproximado hoy:", ["baja (0–39)", "media (40–69)", "alta (70–100)"])
    att_mid = _bucket_to_mid(att_bucket)

    # 3) Filtrar candidatos
    candidates = df.copy()
    if user_cat and cat_col:
        candidates = candidates[candidates[cat_col].astype(str).str.contains(user_cat.split()[0], case=False, na=False)]

    # Ordenar por cercanía de atención
    if "attention_num" in candidates.columns:
        candidates["__dist"] = (candidates["attention_num"].fillna(att_mid) - att_mid).abs()
        candidates = candidates.sort_values("__dist")
    else:
        candidates["__dist"] = 0.0

    # Tomar hasta 3 opciones
    candidates = candidates.head(3)
    if candidates.empty:
        print("No encontré coincidencias. Intenta de nuevo con otra categoría o usa el modo manual.")
        return None

    # Mostrar opciones amigables con FB-ID
    print("\nEncontré estas opciones. Elige tu código FB-ID:")
    for _, r in candidates.iterrows():
        fb = int(r.get("fb_id", 0))
        at = r.get("attention_num", None)
        at_bucket = _bucket_attention(at)
        cat_show = str(r.get(cat_col, "Sin categoría")).split("(")[0].strip() if cat_col else "Sin categoría"
        print(f"- FB-ID {fb} | Categoría: {cat_show} | Atención: {at_bucket}")

    while True:
        raw = input("Escribe tu FB-ID (o 'q' para cancelar): ").strip()
        if raw.lower() == "q":
            return None
        idx = _find_index_by_fbid(df, raw)
        if idx is not None:
            return idx
        print("FB-ID inválido. Intenta de nuevo.")


# ---------- API que usa main.py ----------

def pick_record_simple(df: pd.DataFrame) -> Optional[int]:
    """
    Selección súper simple para pruebas:
    - Muestra cuántos registros hay.
    - Pide un número entre 0 y N-1.
    - No imprime tablas ni categorías.
    """
    n = len(df)
    if n == 0:
        print("No hay registros en el grupo objetivo.")
        return None

    print(f"\nHay {n} registros del grupo objetivo (Student + Smartphone).")
    print("Para probar, ingresa un número de registro entre 0 y", n - 1, "(o 'q' para cancelar).")

    while True:
        raw = input("Número de registro: ").strip()
        if raw.lower() == "q":
            return None
        if raw.isdigit():
            idx = int(raw)
            if 0 <= idx < n:
                return idx
        print("Valor inválido. Debe ser un número entre 0 y", n - 1, "o 'q' para cancelar.")


def compute_score_for_row(df: pd.DataFrame, mapping: Dict[str, Optional[str]], idx: int) -> Tuple[float, float, float, float]:
    fs = FocusScore()
    row = df.iloc[idx].to_dict()

    # Atención numérica (derivada)
    attention = 0.0
    if mapping["attention"] and pd.notna(row.get(mapping["attention"])):
        try:
            attention = float(row.get(mapping["attention"]))
        except (TypeError, ValueError):
            attention = 0.0

    # Tiempo social (horas) derivado
    social_time = 0.0
    if mapping["social"] and pd.notna(row.get(mapping["social"])):
        try:
            social_time = float(row.get(mapping["social"]))
        except (TypeError, ValueError):
            social_time = 0.0

    # Notificaciones (exacta o estimada)
    notifications = 30.0
    notif_col_exact = next((c for c in df.columns if "notifications" == c), None)
    if notif_col_exact and pd.notna(row.get(notif_col_exact)):
        try:
            notifications = float(row.get(notif_col_exact))
        except (TypeError, ValueError):
            notifications = 30.0
    else:
        notif_handling = next((c for c in df.columns if "notification_handling" in c), None)
        if notif_handling:
            notifications = _notifications_from_handling_text(row.get(notif_handling))

    score = fs.compute(attention=attention, social_time=social_time, notifications=notifications)
    _friendly_report(score, attention, social_time, notifications)
    return score, attention, social_time, notifications

def manual_entry_with_recs(log_path: str = "./src/logs/focusboost_log.csv") -> None:
    """
    Ingreso manual (hoy) — versión guiada sin pedir números “imposibles”.
    Preguntas por categorías fáciles y convertimos a valores internos aproximados.
    """
    print("\n== Ingreso manual (hoy) ==")

    # 1) Atención aproximada (elige una)
    att_choice = _choose_from_list(
        "¿Cómo describirías tu nivel de atención hoy?",
        [
            "Baja (me distraigo rápido, <15 min seguidos)",
            "Media (aguanto unos 30–45 min)",
            "Alta (puedo mantener ~1 hora o más)"
        ]
    )
    att_map = {
        "Baja (me distraigo rápido, <15 min seguidos)": 25.0,
        "Media (aguanto unos 30–45 min)": 55.0,
        "Alta (puedo mantener ~1 hora o más)": 85.0,
    }
    attention = att_map.get(att_choice, 55.0)

    # 2) Tiempo en apps que distraen (elige una)
    st_choice = _choose_from_list(
        "¿Cuánto usaste apps que te distraen hoy (en total)?",
        [
            "Casi nada (≤ 30 min)",
            "Poco (30–60 min)",
            "Algo (1–2 h)",
            "Moderado (2–3 h)",
            "Alto (> 3 h)"
        ]
    )
    st_map = {
        "Casi nada (≤ 30 min)": 0.5,
        "Poco (30–60 min)": 0.75,
        "Algo (1–2 h)": 1.5,
        "Moderado (2–3 h)": 2.5,
        "Alto (> 3 h)": 3.5,
    }
    social_time = st_map.get(st_choice, 1.5)

    # 3) Notificaciones percibidas (elige una)
    notif_choice = _choose_from_list(
        "¿Cómo estuvieron tus notificaciones hoy?",
        [
            "Silenciadas (modo no molestar / foco)",
            "Gestionadas (resumen inteligente / solo esenciales)",
            "Normales (sin cambios especiales)",
            "Muchas / constantes (me interrumpían seguido)"
        ]
    )
    notif_map = {
        "Silenciadas (modo no molestar / foco)": 10.0,
        "Gestionadas (resumen inteligente / solo esenciales)": 20.0,
        "Normales (sin cambios especiales)": 30.0,
        "Muchas / constantes (me interrumpían seguido)": 60.0,
    }
    notifications = notif_map.get(notif_choice, 30.0)

    # 4) Categoría principal usada (opcional, ayuda a las recomendaciones)
    cat_choice = _choose_from_list(
        "¿Qué usaste más hoy?",
        [
            "Social (Instagram, TikTok, X, etc.)",
            "Streaming (YouTube, Netflix, etc.)",
            "Gaming",
            "Mensajería (WhatsApp, Messenger)",
            "Educación/Estudio",
            "Productividad/Tareas",
            "Otra / No sé"
        ]
    ) or "Otra / No sé"
    app_category = cat_choice

    # 5) Momento de uso principal (para detectar nocturnidad, sin horas exactas)
    daypart = _choose_from_list(
        "¿En qué momento usaste más el teléfono hoy?",
        [
            "Mañana (6–12)",
            "Tarde (12–18)",
            "Noche (18–22)",
            "Nocturno (22–6)"
        ]
    )
    nocturnal = (daypart == "Nocturno (22–6)")

    # --- Cálculo del Focus Score (misma clase y fórmula) ---
    fs = FocusScore()
    score = fs.compute(attention=attention, social_time=social_time, notifications=notifications)

    # Reporte amigable (sin datos crudos raros)
    _friendly_report(score, attention, social_time, notifications)

    # 6) Registro de bloques (opcional, con wording simple)
    resp_blocks = normalize_string(input("¿Quieres registrar tus bloques de estudio hoy? (s/n): ").strip())
    planned = done = adherence = None
    if resp_blocks == "s":
        print("Ok, lo hacemos rápido (si no lo recuerdas exacto, aproxima):")
        planned, done, adherence = track_blocks()

    # 7) Recomendaciones basadas en banderas simples
    actions = {
        "nocturnal": nocturnal,
        "notif_high": notifications >= 60,
        "social_high": (social_time > 3) or ("social" in normalize_string(app_category)),
        "low_attention": attention < 50,
        "adherence_low": (adherence is not None and adherence < 60.0),
    }
    recs = recommend(actions)

    print("\nRecomendaciones:")
    for i, r in enumerate(recs, 1):
        print(f"- {r}")

    # 8) Log amigable (queda igual que antes)
    now = datetime.now().isoformat(timespec="seconds")
    log_row = {
        "timestamp": now,
        "mode": "manual_buckets",
        "attention": attention,
        "social_time": social_time,
        "notifications": notifications,
        "app_category": app_category,
        "nocturnal": nocturnal,
        "focus_score": score,
        "usage_label": classify_usage_hours(social_time),
        "planned_blocks": planned,
        "done_blocks": done,
        "adherence": adherence,
        "attention_label": att_choice,
        "social_label": st_choice,
        "notifications_label": notif_choice,
        "daypart": daypart,
    }
    _append_log(log_path, log_row)
    print(f"\nGuardado en {log_path}")
