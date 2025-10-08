from typing import Callable
from utils import clamp


class FocusScore:
    """
    Puntaje simple de concentración basado en lo visto en clase:
      score = base + w1*attention - w2*social_time - w3*notifications
    Donde:
      - attention: 0..100 (mayor es mejor)
      - social_time: horas en apps distractoras (mayor reduce score)
      - notifications: conteo/índice (mayor reduce score)
    El resultado se recorta a [0, 100].
    """

    def __init__(self, w_attention: float = 1.0, w_social: float = 0.5, w_notif: float = 0.3, base: float = 50.0):
        self.w_attention = w_attention
        self.w_social = w_social
        self.w_notif = w_notif
        self.base = base

    def compute(self, attention: float = 0.0, social_time: float = 0.0, notifications: float = 0.0) -> float:
        try:
            a = float(attention or 0.0)
            s = float(social_time or 0.0)
            n = float(notifications or 0.0)
        except (TypeError, ValueError):
            a, s, n = 0.0, 0.0, 0.0

        score = self.base + self.w_attention * a - self.w_social * s - self.w_notif * n
        return clamp(score, 0.0, 100.0)


def threshold_closure(limit: float) -> Callable[[float], bool]:
    """
    Devuelve una función (clausura) que evalúa si un valor >= limit.
    Ejemplo: is_good = threshold_closure(70.0); is_good(82.5) -> True
    """
    def checker(value: float) -> bool:
        try:
            return float(value) >= float(limit)
        except (TypeError, ValueError):
            return False
    return checker