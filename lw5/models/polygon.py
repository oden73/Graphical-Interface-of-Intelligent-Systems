from typing import List, Optional

from models.point import Point
from models.edge import Edge


class Polygon:
    def __init__(self, points: Optional[List[Point]] = None) -> None:
        self.points: List[Point] = points if points else []

    def add_point(self, point: Point) -> None:
        self.points.append(point)

    def get_edges(self) -> List[Edge]:
        return [
            Edge(self.points[i], self.points[(i + 1) % len(self.points)])
            for i in range(len(self.points))
        ]

    def __repr__(self) -> str:
        return f"Polygon({self.points})"
