from typing import List
from math import atan2

from models.point import Point


def graham_scan(points: List[Point]) -> List[Point]:
    sorted_points: List[Point] = sorted(points, key=lambda p: (p.y, p.x))
    start: Point = sorted_points[0]

    def polar_angle(p: Point) -> float:
        return atan2(p.y - start.y, p.x - start.x)

    sorted_by_angle: List[Point] = sorted(sorted_points[1:], key=polar_angle)
    hull: List[Point] = [start, sorted_by_angle[0]]

    for point in sorted_by_angle[1:]:
        while len(hull) >= 2:
            dx1: float = hull[-1].x - hull[-2].x
            dy1: float = hull[-1].y - hull[-2].y
            dx2: float = point.x - hull[-1].x
            dy2: float = point.y - hull[-1].y
            cross: float = dx1 * dy2 - dy1 * dx2

            if cross > 0:
                break
            hull.pop()

        hull.append(point)

    return hull


def jarvis_march(points: List[Point]) -> List[Point]:
    if len(points) < 3:
        return points.copy()

    hull: List[Point] = []
    leftmost: Point = min(points, key=lambda p: p.x)
    point_on_hull: Point = leftmost

    while True:
        hull.append(point_on_hull)
        endpoint: Point = points[0]
        for candidate in points[1:]:
            if endpoint == point_on_hull:
                endpoint = candidate
            else:
                dx1: float = endpoint.x - point_on_hull.x
                dy1: float = endpoint.y - point_on_hull.y
                dx2: float = candidate.x - point_on_hull.x
                dy2: float = candidate.y - point_on_hull.y
                cross: float = dx1 * dy2 - dy1 * dx2

                if cross < 0 or (cross == 0 and
                                 ((candidate.x - point_on_hull.x) ** 2 + (candidate.y - point_on_hull.y) ** 2) >
                                 ((endpoint.x - point_on_hull.x) ** 2 + (endpoint.y - point_on_hull.y) ** 2)):
                    endpoint = candidate

        point_on_hull = endpoint
        if endpoint == leftmost:
            break

    return hull
