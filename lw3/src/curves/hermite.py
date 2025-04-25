import numpy as np

from .curve import Curve
from src.math.geometry import subtract_points
from src.math.matrix_operations import hermite_basis_matrix, apply_matrix


class HermiteCurve(Curve):
    def __init__(self, p1, p4, r1=None, r4=None):
        self.p1 = np.array(p1)
        self.p4 = np.array(p4)

        if r1 is None or r4 is None:
            delta = subtract_points(self.p4, self.p1)
            self.r1 = delta
            self.r4 = delta
        else:
            self.r1 = np.array(r1)
            self.r4 = np.array(r4)

        super().__init__([self.p1, self.p4, self.r1, self.r4])

    def get_points(self, num_points=100):
        M = hermite_basis_matrix()

        Gx = np.array([self.p1[0], self.p4[0], self.r1[0], self.r4[0]])
        Gy = np.array([self.p1[1], self.p4[1], self.r1[1], self.r4[1]])

        coeffs_x = apply_matrix(M, Gx)
        coeffs_y = apply_matrix(M, Gy)

        t_values = np.linspace(0, 1, num_points)
        points = []

        for t in t_values:
            T = np.array([t**3, t**2, t, 1])
            x = T @ coeffs_x
            y = T @ coeffs_y
            points.append((x, y))

        return points
