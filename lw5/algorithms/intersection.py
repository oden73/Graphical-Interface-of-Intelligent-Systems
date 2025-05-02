from typing import List

from models.point import Point
from models.polygon import Polygon


def ccw(a: Point, b: Point, c: Point) -> bool:
    return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)


def segments_intersect(p1: Point, p2: Point, q1: Point, q2: Point) -> bool:
    a: Point = p1
    b: Point = p2
    c: Point = q1
    d: Point = q2

    return (ccw(a, c, d) != ccw(b, c, d)) and (ccw(a, b, c) != ccw(a, b, d))


def segment_intersects_polygon(p1: Point, p2: Point, polygon: Polygon) -> bool:
    points: List[Point] = polygon.points
    num_points: int = len(points)

    for i in range(num_points):
        q1: Point = points[i]
        q2: Point = points[(i + 1) % num_points]
        if segments_intersect(p1, p2, q1, q2):
            return True

    return False
