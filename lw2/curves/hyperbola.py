from curves.curve import Curve
from typing import Generator


class Hyperbola(Curve):
    required_params = ['center_x', 'center_y', 'a', 'b']

    def __init__(self, center_x: int, center_y: int, a: int, b: int) -> None:
        super().__init__()
        self.parameters = {
            'center_x': center_x,
            'center_y': center_y,
            'a': a,
            'b': b
        }

    def get_points(self) -> list[tuple[int, int]]:
        return [point for step in self.step_by_step() for point in step['points']]

    def step_by_step(self) -> Generator[dict, None, None]:
        x0 = self.parameters['center_x']
        y0 = self.parameters['center_y']
        a = max(2, self.parameters['a'])
        b = max(2, self.parameters['b'])

        a2 = a * a
        b2 = b * b
        MAX_X = 200

        for y in range(0, 101):
            try:
                x_sq = a2 * (1 + (y * y) / b2)
                x = int(x_sq ** 0.5)
            except ZeroDivisionError:
                continue
            except ValueError:
                continue

            if x > MAX_X:
                continue

            points = [
                (x0 + x, y0 + y), (x0 + x, y0 - y),
                (x0 - x, y0 + y), (x0 - x, y0 - y)
            ]

            yield {
                'points': points,
                'x': x,
                'y': y,
                'delta': 0
            }

    @staticmethod
    def _reflect_points(x0, y0, x, y) -> list[tuple[int, int]]:
        return [
            (x0 + x, y0 + y), (x0 + x, y0 - y),
            (x0 - x, y0 + y), (x0 - x, y0 - y)
        ]
