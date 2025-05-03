from typing import List
import math

from models.point import Point
from models.polygon import Polygon


def is_point_in_polygon(point: Point, polygon: Polygon) -> bool:
    points: List[Point] = polygon.points
    num_points: int = len(points)

    intersections: int = 0

    for i in range(num_points):
        p1: Point = points[i]
        p2: Point = points[(i + 1) % num_points]
        
        if ((p1.y > point.y) != (p2.y > point.y)) and \
                (point.x < (p2.x - p1.x) * (point.y - p1.y) / (p2.y - p1.y) + p1.x):
            intersections += 1

    return intersections % 2 == 1
