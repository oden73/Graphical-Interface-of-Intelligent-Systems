from typing import List

from models.point import Point
from models.polygon import Polygon


def is_point_in_polygon(point: Point, polygon: Polygon) -> bool:
    x: float = point.x
    y: float = point.y
    points: List[Point] = polygon.points
    num_points: int = len(points)
    inside: bool = False

    j: int = num_points - 1
    for i in range(num_points):
        xi: float = points[i].x
        yi: float = points[i].y
        xj: float = points[j].x
        yj: float = points[j].y

        intersect: bool = ((yi > y) != (yj > j)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-10) + xi)
        if intersect:
            inside = not inside
        j = i

    return inside
