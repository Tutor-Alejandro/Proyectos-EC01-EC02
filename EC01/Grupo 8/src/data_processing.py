from typing import Dict, Optional
import pandas as pd


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    return df


def _to_float_hours(text: str) -> Optional[float]:
    """
    Convierte textos como '4–6', '6-8', 'More than 10' a un valor (promedio o tope razonable).
    Devuelve None si no es interpretable.
    """
    if not isinstance(text, str):
        return None
    t = text.strip().lower().replace("—", "-").replace("–", "-")
    # Rangos del tipo "4-6"
    if "-" in t:
        parts = t.split("-")
        try:
            lo = float(parts[0])
            hi = float(parts[1])
            return (lo + hi) / 2.0
        except:
            return None
    # Frases comunes
    if "more than 10" in t or "más de 10" in t:
        return 10.5
    if "8-10" in t:
        return 9.0  # ya cubierto por rango, redundancia defensiva
    if t.isdigit():
        return float(t)
    # Último recurso: intenta extraer primer número
    import re
    m = re.search(r"(\d+(\.\d+)?)", t)
    if m:
        return float(m.group(1))
    return None


def _attention_text_to_score(text: str) -> Optional[float]:
    """
    Mapea atención textual a un valor 0..100 aproximado (heurístico, suficiente para el curso).
    """
    if not isinstance(text, str):
        return None
    t = text.strip().lower()
    # Orden de menor a mayor atención
    if "less than 10" in t or "menos de 10" in t:
        return 20.0
    if "10–30" in t or "10-30" in t:
        return 40.0
    if "30–60" in t or "30-60" in t:
        return 60.0
    if "more than 1 hour" in t or "más de 1 hora" in t:
        return 85.0
    # fallback: intenta número directo si viene como "75"
    try:
        v = float(t)
        return max(0.0, min(100.0, v))
    except:
        return None


def load_and_filter(csv_path: str) -> pd.DataFrame:
    """
    Lee el CSV, normaliza columnas y filtra a Student + Smartphone.
    Además, crea columnas numéricas derivadas:
      - attention_num (0..100)
      - screen_time_hours (float)
    """
    df = pd.read_csv(csv_path)
    df = _normalize_columns(df)

    occ = next((c for c in df.columns if "occup" in c), "occupation")
    dev = next((c for c in df.columns if "device" in c or "dispositivo" in c), "device")

    df = df[df[occ].astype(str).str.strip().str.lower() == "student"]
    df = df[df[dev].astype(str).str.strip().str.lower() == "smartphone"]

    # Detectar posibles nombres para columnas de interés
    att_col = next((c for c in df.columns if "attention" in c or "span" in c), None)
    scr_col = next((c for c in df.columns if "average_screen_time" in c or ("screen" in c and "time" in c)), None)

    # Derivar numéricos
    if att_col:
        df["attention_num"] = df[att_col].apply(_attention_text_to_score)
    else:
        df["attention_num"] = None

    if scr_col:
        df["screen_time_hours"] = df[scr_col].apply(_to_float_hours)
    else:
        df["screen_time_hours"] = None

    return df


def guess_columns(df: pd.DataFrame) -> Dict[str, Optional[str]]:
    """
    Devuelve mapeo de columnas lógicas del proyecto.
    Preferimos las derivadas numéricas si existen.
    """
    mapping = {"attention": None, "social": None, "notif": None, "name": None, "app_category": None}

    # Preferir columnas derivadas
    if "attention_num" in df.columns:
        mapping["attention"] = "attention_num"
    if "screen_time_hours" in df.columns:
        mapping["social"] = "screen_time_hours"

    # Si no hubiese derivadas, caer a heurísticas originales
    for c in df.columns:
        lc = c.lower()
        if mapping["attention"] is None and ("attention" in lc or "span" in lc):
            mapping["attention"] = c
        if mapping["social"] is None and ("average_screen_time" in lc or ("screen" in lc and "time" in lc)):
            mapping["social"] = c
        if mapping["notif"] is None and ("notif" in lc):
            mapping["notif"] = c
        if mapping["name"] is None and ("name" in lc or "student" in lc):
            mapping["name"] = c
        if mapping["app_category"] is None and ("app_category" in lc or "category" in lc or "activity" in lc):
            mapping["app_category"] = c

    return mapping
