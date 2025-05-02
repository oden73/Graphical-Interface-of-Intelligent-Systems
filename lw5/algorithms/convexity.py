from typing import List, Tuple

from models.point import Point
from models.polygon import Polygon


def is_convex(polygon: Polygon) -> bool:
    points: List[Point] = polygon.points
    num_points: int = len(points)
    if num_points < 3:
        return False

    sign: float = 0.0
    for i in range(num_points):
        dx1: float = points[(i + 1) % num_points].x - points[i].x
        dy1: float = points[(i + 1) % num_points].y - points[i].y
        dx2: float = points[(i + 2) % num_points].x - points[(i + 1) % num_points].x
        dy2: float = points[(i + 2) % num_points].y - points[(i + 1) % num_points].y
        z_cross_product: float = dx1 * dy2 - dx2 * dy1

        if z_cross_product != 0:
            if sign == 0:
                sign = z_cross_product
            elif sign * z_cross_product < 0:
                return False

    return True


def compute_internal_normals(polygon: Polygon) -> List[Tuple[float, float]]:
    points: List[Point] = polygon.points
    num_points: int = len(points)
    normals: List[Tuple[float, float]] = []

    for i in range(num_points):
        p1: Point = points[i]
        p2: Point = points[(i + 1) % num_points]
        edge_dx: float = p2.x - p1.x
        edge_dy: float = p2.y - p1.y

        normal_x: float = -edge_dy
        normal_y: float = edge_dx

        length: float = (normal_x ** 2 + normal_y ** 2) ** 0.5
        if length != 0:
            normal_x /= length
            normal_y /= length

        normals.append((normal_x, normal_y))

    return normals
