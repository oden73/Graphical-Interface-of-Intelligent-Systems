from typing import List
from PyQt5.QtCore import QPointF


def jarvis_march(points: List[QPointF]) -> List[QPointF]:
    def orientation(p: QPointF, q: QPointF, r: QPointF) -> int:
        val: float = (q.y() - p.y()) * (r.x() - q.x()) - (q.x() - p.x()) * (r.y() - q.y())
        if val == 0.:
            return 0  # коллинеарны
        return 1 if val > 0 else 2  # 1 - по часовой, 2 - против

    if len(points) < 3:
        return points.copy()

    hull: List[QPointF] = []
    leftmost: int = min(
        range(len(points)),
        key=lambda i: (points[i].x(), points[i].y())
    )
    p: int = leftmost

    while True:
        hull.append(points[p])
        q: int = (p + 1) % len(points)

        for i in range(len(points)):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i

        p = q
        if p == leftmost:
            break

    return hull
