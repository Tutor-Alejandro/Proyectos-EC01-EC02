from typing import Tuple


def _ask_int(prompt: str, lo: int = 0, hi: int = 100, default: int | None = None) -> int:
    while True:
        raw = input(f"{prompt} ").strip()
        if raw == "" and default is not None:
            return default
        if raw.isdigit():
            val = int(raw)
            if lo <= val <= hi:
                return val
        print("Valor inválido. Intenta de nuevo.")


def track_blocks() -> Tuple[int, int, float]:
    """Solicita bloques planificados/completados y calcula adherencia porcentual."""
    print("\n== Seguimiento de bloques (Pomodoro/Time-boxing) ==")
    planned = _ask_int("¿Cuántos bloques planificaste hoy? (0-20):", 0, 20, 0)
    done = _ask_int("¿Cuántos bloques completaste sin interrupciones? (0-20):", 0, 20, 0)
    adherence = 0.0 if planned == 0 else (done / planned) * 100.0
    print(f"Adherencia: {adherence:.1f}%")
    return planned, done, adherence