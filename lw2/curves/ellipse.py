from curves.curve import Curve
from typing import Generator


class Ellipse(Curve):
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
        a = self.parameters['a']
        b = self.parameters['b']

        a2 = a * a
        b2 = b * b
        x = 0
        y = b

        # Начальное значение ошибки
        delta = b2 - a2 * b + 0.25 + a2
        dx = 0
        dy = 2 * a2 * y

        # Первая зона
        while dx < dy:
            yield {
                'points': self._reflect_points(x0, y0, x, y),
                'x': x, 'y': y, 'delta': delta
            }

            if delta < 0:
                x += 1
                dx += 2 * b2
                delta += dx + b2
            else:
                x += 1
                y -= 1
                dx += 2 * b2
                dy -= 2 * a2
                delta += dx - dy + b2

        # Вторая зона
        delta = b2 * (x + 0.5) ** 2 + a2 * (y - 1) ** 2 - a2 * b2
        while y >= 0:
            yield {
                'points': self._reflect_points(x0, y0, x, y),
                'x': x, 'y': y, 'delta': delta
            }

            if delta > 0:
                y -= 1
                dy -= 2 * a2
                delta += a2 - dy
            else:
                x += 1
                y -= 1
                dx += 2 * b2
                dy -= 2 * a2
                delta += dx - dy + a2

    @staticmethod
    def _reflect_points(x0: int, y0: int, x: int, y: int) -> list[tuple[int, int]]:
        return [
            (x0 + x, y0 + y), (x0 - x, y0 + y),
            (x0 + x, y0 - y), (x0 - x, y0 - y)
        ]
