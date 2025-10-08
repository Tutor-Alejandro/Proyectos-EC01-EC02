from typing import Dict, List
from utils import normalize_string


def classify_usage_hours(hours: float) -> str:
    """Clasifica uso total en horas: bajo ≤1.5; moderado ≤3; alto >3."""
    try:
        h = float(hours)
    except (TypeError, ValueError):
        return "desconocido"
    if h <= 1.5:
        return "bajo"
    if h <= 3.0:
        return "moderado"
    return "alto"


def recommend(actions: Dict[str, bool]) -> List[str]:
    """
    Genera recomendaciones a partir de banderas (flags):
    - nocturnal: uso nocturno relevante (>=22:00)
    - notif_high: notificaciones elevadas (p. ej., >=60)
    - social_high: uso social elevado (>3h o categoría Social)
    - low_attention: atención baja (<50)
    - adherence_low: adherencia a bloques <60%
    """
    recs: List[str] = []

    if actions.get("nocturnal"):
        recs.append("Evita uso nocturno (>22:00). Activa 'modo descanso' o apaga notificaciones nocturnas.")
    if actions.get("notif_high"):
        recs.append("Silencia o resume notificaciones. Prioriza solo apps esenciales en horario de estudio.")
    if actions.get("social_high"):
        recs.append("Reubica apps sociales fuera de la pantalla principal durante bloques de estudio.")
    if actions.get("low_attention"):
        recs.append("Planifica bloques cortos (25 min) con pausas. Comienza con 2–3 bloques.")
    if actions.get("adherence_low"):
        recs.append("Reduce el objetivo de bloques y sube gradualmente. Celebra el progreso.")

    if not recs:
        recs.append("Vas bien. Mantén hábitos consistentes y revisa avances semanalmente.")
    return recs