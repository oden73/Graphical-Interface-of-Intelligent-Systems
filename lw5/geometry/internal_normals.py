from typing import List, Tuple
from PyQt5.QtCore import QPointF
import math


def compute_internal_normals(polygon: List[QPointF]) -> List[Tuple[Tuple[int, int], Tuple[float, float]]]:
    normals: List[Tuple[Tuple[int, int], Tuple[float, float]]] = []
    n: int = len(polygon)

    for i in range(n):
        p1: QPointF = polygon[i]
        p2: QPointF = polygon[(i + 1) % n]

        dx: float = p2.x() - p1.x()
        dy: float = p2.y() - p1.y()

        nx: float = dy
        ny: float = -dx

        length: float = math.hypot(nx, ny)
        if length == 0:
            continue
        nx /= length
        ny /= length

        mx: float = (p1.x() + p2.x()) / 2
        my: float = (p1.y() + p2.y()) / 2
        midpoint: Tuple[int, int] = int(mx), int(my)
        normal_vector: Tuple[float, float] = nx, ny

        normals.append((midpoint, normal_vector))

    return normals
