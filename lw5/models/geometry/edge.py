from models.geometry.point import Point


class Edge:
    def __init__(self, start: Point, end: Point) -> None:
        self.start: Point = start
        self.end: Point = end

    def __repr__(self) -> str:
        return f"Edge({self.start}, {self.end})"
