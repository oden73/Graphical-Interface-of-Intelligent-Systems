from typing import List
from PyQt5.QtCore import QPointF


def is_convex(polygon: List[QPointF], epsilon: float = 1e-6) -> bool:
    def cross(o: QPointF, a: QPointF, b: QPointF) -> float:
        return (a.x() - o.x()) * (b.y() - o.y()) - (a.y() - o.y()) * (b.x() - o.x())

    n: int = len(polygon)
    if n < 3:
        return False

    sign: int = 0
    for i in range(n):
        o: QPointF = polygon[i]
        a: QPointF = polygon[(i + 1) % n]
        b: QPointF = polygon[(i + 2) % n]
        c: float = cross(o, a, b)

        if abs(c) < epsilon:
            continue

        current_sign: int = 1 if c > 0 else -1
        if sign == 0:
            sign = current_sign
        elif sign != current_sign:
            return False

    return sign != 0
