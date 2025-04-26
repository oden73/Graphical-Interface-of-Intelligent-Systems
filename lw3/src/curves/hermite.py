import numpy as np


from src.curves.curve import Curve
from src.math.geometry import subtract_points
from src.math.matrix_operations import hermite_basis_matrix, apply_matrix


class HermiteCurve(Curve):
    def __init__(self, control_points):
        super().__init__(control_points)

        self.points = [np.array(p) for p in control_points]
        self.tangents = self._generate_tangents(self.points)

    @staticmethod
    def _generate_tangents(points):
        tangents = []
        n = len(points)

        for i in range(n):
            if i == 0:
                # Первая точка: R0 = P1 - P0
                tangent = subtract_points(points[1], points[0])
            elif i == n - 1:
                # Последняя точка: Rn = Pn - Pn-1
                tangent = subtract_points(points[-1], points[-2])
            else:
                # Внутренние точки: среднее между соседями
                tangent = 0.5 * subtract_points(points[i + 1], points[i - 1])

            tangents.append(tangent)
        return tangents

    def get_points(self, num_points=100):
        if len(self.points) < 2:
            return []

        curve_points = []
        M = hermite_basis_matrix()

        segments = len(self.points) - 1
        points_per_segment = max(2, num_points // segments)

        for i in range(segments):
            p0 = self.points[i]
            p1 = self.points[i + 1]
            r0 = self.tangents[i]
            r1 = self.tangents[i + 1]

            Gx = np.array([p0[0], p1[0], r0[0], r1[0]])
            Gy = np.array([p0[1], p1[1], r0[1], r1[1]])

            coeffs_x = apply_matrix(M, Gx)
            coeffs_y = apply_matrix(M, Gy)

            for j in range(points_per_segment):
                t = j / (points_per_segment - 1)
                T = np.array([t**3, t**2, t, 1])
                x = T @ coeffs_x
                y = T @ coeffs_y
                curve_points.append((x, y))

        return curve_points
