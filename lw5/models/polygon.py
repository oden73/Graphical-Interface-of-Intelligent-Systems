from PyQt5.QtCore import QPointF
from typing import List, Tuple


class Polygon:
    points: List[QPointF]

    def __init__(self, points: List[QPointF] = None) -> None:
        if points is None:
            points = []

        self.points: List[QPointF] = points

    def add_point(self, point: QPointF) -> None:
        self.points.append(point)

    def clear(self) -> None:
        self.points.clear()

    def get_edges(self) -> List[Tuple[QPointF, QPointF]]:
        edges: List[Tuple[QPointF, QPointF]] = []
        n: int = len(self.points)
        for i in range(n):
            edges.append((self.points[i], self.points[(i + 1) % n]))
        return edges

    def get_closed_edges(self) -> List[Tuple[QPointF, QPointF]]:
        edges: List[Tuple[QPointF, QPointF]] = []
        n: int = len(self.points)
        if n < 2:
            return edges
        for i in range(n - 1):
            edges.append((self.points[i], self.points[i + 1]))
        edges.append((self.points[-1], self.points[0]))
        return edges

    def is_closed(self) -> bool:
        return len(self.points) > 2
