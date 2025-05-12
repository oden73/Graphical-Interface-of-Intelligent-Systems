from PyQt5.QtCore import QPointF
from typing import List, Optional


def find_segment_polygon_intersection(segment_start: QPointF, segment_end: QPointF, polygon: List[QPointF]) -> List[QPointF]:
    def segment_intersection(p1: QPointF, p2: QPointF, q1: QPointF, q2: QPointF) -> Optional[QPointF]:
        def det(a, b):
            return a.x() * b.y() - a.y() * b.x()

        r = QPointF(p2.x() - p1.x(), p2.y() - p1.y())
        s = QPointF(q2.x() - q1.x(), q2.y() - q1.y())

        denom = det(r, s)
        if denom == 0:
            return None  # параллельны или совпадают

        qp = QPointF(q1.x() - p1.x(), q1.y() - p1.y())
        t = det(qp, s) / denom
        u = det(qp, r) / denom

        if 0 <= t <= 1 and 0 <= u <= 1:
            intersection = QPointF(p1.x() + t * r.x(), p1.y() + t * r.y())
            return intersection
        return None

    intersections = []
    n = len(polygon)
    for i in range(n):
        poly_start = polygon[i]
        poly_end = polygon[(i + 1) % n]
        point = segment_intersection(segment_start, segment_end, poly_start, poly_end)
        if point is not None:
            intersections.append(point)
    return intersections
