from curves.curve import Curve
from typing import Generator


class Circle(Curve):
    required_params = ['center_x', 'center_y', 'radius']

    def __init__(self, center_x: int, center_y: int, radius: int = 10) -> None:
        super().__init__()

        self.parameters = {
            'center_x': center_x,
            'center_y': center_y,
            'radius': radius
        }

    def get_points(self) -> list[tuple[int, int]]:
        # using bresenham algorithm

        points: list[tuple[int, int]] = []
        x0: int = self.parameters['center_x']
        y0: int = self.parameters['center_y']
        radius: int = self.parameters['radius']

        x: int = 0
        y: int = radius
        delta: int = 1 - 2 * radius

        while y >= x:
            # symmetrical display in 8 octant
            points.extend([
                (x0 + x, y0 + y),
                (x0 - x, y0 + y),
                (x0 + x, y0 - y),
                (x0 - x, y0 - y),
                (x0 + y, y0 + x),
                (x0 - y, y0 + x),
                (x0 + y, y0 - x),
                (x0 - y, y0 - x)
            ])

            # next step calculation
            x += 1
            if delta < 0:
                error: int = 2 * delta + 2 * y - 1
                if error <= 0:
                    delta += 2 * x + 1
                else:
                    y -= 1
                    delta += 2 * (x - y + 1)
            else:
                y -= 1
                delta += 2 * (x - y + 1)

        return points

    def step_by_step(self) -> Generator[dict, None, None]:
        x0: int = self.parameters['center_x']
        y0: int = self.parameters['center_y']
        radius: int = self.parameters['radius']

        x: int = 0
        y: int = radius
        delta: int = 1 - 2 * radius

        while y >= x:
            # current state return
            step_data: dict[str, any] = {
                'points': [
                    (x0 + x, y0 + y),
                    (x0 - x, y0 + y),
                    (x0 + x, y0 - y),
                    (x0 - x, y0 - y),
                    (x0 + y, y0 + x),
                    (x0 - y, y0 + x),
                    (x0 + y, y0 - x),
                    (x0 - y, y0 - x)
                ],
                'delta': delta,
                'x': x,
                'y': y
            }
            yield step_data

            # next step calculation
            x += 1
            if delta < 0:
                error: int = 2 * delta + 2 * y - 1
                if error <= 0:
                    delta += 2 * x + 1
                else:
                    y -= 1
                    delta += 2 * (x - y + 1)
            else:
                y -= 1
                delta += 2 * (x - y + 1)
