from typing import List
import math

from models.point import Point
from models.polygon import Polygon


def is_point_in_polygon(point: Point, polygon: Polygon) -> bool:
    def angle_between(p1: Point, p2: Point, p: Point) -> float:
        dx1: float = p1.x - p.x
        dy1: float = p1.y - p.y
        dx2: float = p2.x - p.x
        dy2: float = p2.y - p.y

        angle1: float = math.atan2(dy1, dx1)
        angle2: float = math.atan2(dy2, dx2)
        angle: float = angle2 - angle1

        if angle <= -math.pi:
            angle += 2 * math.pi
        elif angle > math.pi:
            angle -= 2 * math.pi

        return angle

    total_angle: float = 0.
    n: int = len(polygon.points)
    for i in range(n):
        p1: Point = polygon.points[i]
        p2: Point = polygon.points[(i + 1) % n]
        total_angle += angle_between(p1, p2, point)

    return abs(abs(total_angle) - 2 * math.pi) < 1e-4
