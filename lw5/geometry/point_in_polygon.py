from typing import List
from PyQt5.QtCore import QPointF


def is_point_inside_polygon(point: QPointF, polygon: List[QPointF]) -> bool:
    x: float = point.x()
    y: float = point.y()
    inside: bool = False
    n: int = len(polygon)

    for i in range(n):
        p1: QPointF = polygon[i]
        p2: QPointF = polygon[(i + 1) % n]

        if (p1.y() > y) != (p2.y() > y):
            x_intersect: float = (p2.x() - p1.x()) * (y - p1.y()) / (p2.y() - p1.y() + 1e-12) + p1.x()
            if x < x_intersect:
                inside = not inside

    return inside
