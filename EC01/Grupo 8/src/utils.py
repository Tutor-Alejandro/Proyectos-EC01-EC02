from typing import Any, Callable, Iterable, List, Tuple, Dict


def normalize_string(s: Any) -> str:
    """Convierte a string, recorta espacios y pasa a minúsculas."""
    return str(s).strip().lower()


def clamp(v: float, lo: float, hi: float) -> float:
    """Restringe v al rango [lo, hi]."""
    return max(lo, min(hi, v))


def list_unique(seq: Iterable[Any]) -> List[Any]:
    """Elimina duplicados preservando el orden (sin usar set directamente)."""
    seen = {}
    out = []
    for x in seq:
        if x not in seen:
            seen[x] = True
            out.append(x)
    return out


def map_count(seq: Iterable[Any]) -> Dict[Any, int]:
    """Cuenta frecuencias de elementos en una secuencia usando dict."""
    counts = {}
    for x in seq:
        counts[x] = counts.get(x, 0) + 1
    return counts


def bubble_sort(items: Iterable[Any], key: Callable[[Any], Any] = lambda x: x, reverse: bool = False) -> List[Any]:
    """
    Algoritmo clásico Bubble Sort.
    - items: lista o iterable
    - key: función para extraer la clave de comparación
    - reverse: True para orden descendente
    """
    arr = list(items)
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            cond = (key(arr[j]) > key(arr[j + 1]) and not reverse) or \
                   (key(arr[j]) < key(arr[j + 1]) and reverse)
            if cond:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr