import numpy as np

from src.curves.curve import Curve


class BSplineCurve(Curve):
    def __init__(self, control_points, degree=3) -> None:
        super().__init__(control_points)
        self.degree = degree
        self.knot_vector = self._generate_uniform_knot_vector(len(control_points), degree)

    @staticmethod
    def _generate_uniform_knot_vector(num_points, degree):
        n = num_points - 1
        k = degree
        m = n + k + 1
        return [0] * k + list(range(m - 2 * k + 1)) + [m - 2 * k] * k

    def _de_boor(self, k, i, t, knots, ctrl_pts):
        if k == 0:
            return np.array(ctrl_pts[i])

        alpha = (t - knots[i]) / (knots[i + self.degree] - knots[i])
        left = self._de_boor(k - 1, i - 1, t, knots, ctrl_pts)
        right = self._de_boor(k - 1, i , t, knots, ctrl_pts)
        return (1 - alpha) * left + alpha * right

    def get_points(self, num_points=100) -> list:
        points = []
        t_start = self.knot_vector[self.degree]
        t_end = self.knot_vector[-self.degree - 1]
        t_values = np.linspace(t_start, t_end, num_points)

        for t in t_values:
            for i in range(len(self.control_points)):
                if self.knot_vector[i] <= t < self.knot_vector[i + 1]:
                    points.append(self._de_boor(self.degree, i, t, self.knot_vector, self.control_points))
                    break

        return points
