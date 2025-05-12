from typing import List, Tuple


def bresenham(x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
    points: List[Tuple[int, int]] = []

    dx: int = abs(x1 - x0)
    dy: int = abs(y1 - y0)
    x, y = x0, y0

    sx: int = 1 if x0 < x1 else -1
    sy: int = 1 if y0 < y1 else -1

    if dx > dy:
        err: int = dx // 2
        while x != x1:
            points.append((x, y))
            err -= dy

            if err < 0:
                y += sy
                err += dx

            x += sy

    points.append((x1, y1))
    return points
