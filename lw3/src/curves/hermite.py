import numpy as np

from src.curves.curve import Curve


class HermiteCurve(Curve):
    def __init__(self, p1, p4, r1, r4) -> None:
        super().__init__([p1, p4, r1, r4])
        self.p1 = np.array(p1)
        self.p4 = np.array(p4)
        self.r1 = np.array(r1)
        self.r4 = np.array(r4)

    def get_points(self, num_points=100) -> list:
        M = np.array([
            [2, -2, 1, 1],
            [-3, 3, -2, -1],
            [0, 0, 1, 0],
            [1, 0, 0, 0]
        ])

        Gx = np.array([self.p1[0], self.p4[0], self.r1[0], self.r4[0]])
        Gy = np.array([self.p1[1], self.p4[1], self.r1[1], self.r4[1]])

        coeffs_x = M @ Gx
        coeffs_y = M @ Gy

        t_values = np.linspace(0, 1, num_points)
        points = []
        for t in t_values:
            T = np.array([t**3, t**2, t, 1])
            x = T @ coeffs_x
            y = T @ coeffs_y
            points.append((x, y))

        return points
