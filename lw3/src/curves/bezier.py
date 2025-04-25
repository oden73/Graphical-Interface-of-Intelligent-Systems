import numpy as np

from src.curves.curve import Curve


class BezierCurve(Curve):
    def get_points(self, num_points=100) -> list:
        def bernstein(i, n, t):
            from math import comb
            return comb(n, i) * (t**i) * ((1 - t)**(n - i))

        n = len(self.control_points) - 1
        t_values = np.linspace(0, 1, num_points)
        points = []

        for t in t_values:
            x = sum(bernstein(i, n, t) * p[0] for i, p in enumerate(self.control_points))
            y = sum(bernstein(i, n, t) * p[1] for i, p in enumerate(self.control_points))

        return points
