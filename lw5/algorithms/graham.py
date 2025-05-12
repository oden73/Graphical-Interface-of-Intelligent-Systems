from typing import List
from PyQt5.QtCore import QPointF
import math


def graham_scan(points: List[QPointF]) -> List[QPointF]:

    def polar_angle(p0: QPointF, p1: QPointF) -> float:
        dx: float = p1.x() - p0.x()
        dy: float = p1.y() - p0.y()
        return math.atan2(dy, dx)

    def distance(p0: QPointF, p1: QPointF) -> float:
        return (p1.x() - p0.x()) ** 2 + (p1.y() - p0.y()) ** 2

    def cross(o: QPointF, a: QPointF, b: QPointF) -> float:
        return (a.x() - o.x()) * (b.y() - o.y()) - (a.y() - o.y()) * (b.x() - o.x())

    if len(points) < 3:
        return points.copy()

    start: QPointF = min(points, key=lambda p: (p.y(), p.x()))
    sorted_points: List[QPointF] = sorted(
        points,
        key=lambda p: (polar_angle(start, p), -distance(start, p))
    )

    hull: List[QPointF] = []
    for p in sorted_points:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)

    return hull
