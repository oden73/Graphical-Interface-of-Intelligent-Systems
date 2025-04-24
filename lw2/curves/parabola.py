from curves.curve import Curve
from typing import Generator


class Parabola(Curve):
    required_params = ['center_x', 'center_y', 'p']

    def __init__(self, center_x: int, center_y: int, p: int) -> None:
        super().__init__()
        self.parameters = {
            'center_x': center_x,
            'center_y': center_y,
            'p': p
        }

    def get_points(self) -> list[tuple[int, int]]:
        return [point for step in self.step_by_step() for point in step['points']]

    def step_by_step(self) -> Generator[dict, None, None]:
        x0 = self.parameters['center_x']
        y0 = self.parameters['center_y']
        p = self.parameters['p']

        x, y, delta = 0, 0, 1 - p

        while x < x0 + 100:
            yield {
                'points': self._reflect_points(x0, y0, x, y),
                'x': x, 'y': y, 'delta': delta
            }

            if delta < 0:
                y += 1
                delta += 2 * y + 1
            else:
                x += 1
                delta += -2 * p + 2 * y + 1
                y += 1

    @staticmethod
    def _reflect_points(x0: int, y0: int, x: int, y: int) -> list[tuple[int, int]]:
        return [
            (x0 + x, y0 + y), (x0 + x, y0 - y)
        ]