import numpy as np


def perspective_projection_matrix(d = 1.) -> np.ndarray:
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 1 / d],
        [0, 0, 0, 0]
    ], dtype=float)


def project_points(points, projection_matrix) -> np.ndarray:
    transformed = points @ projection_matrix.T
    with np.errstate(divide='ignore', invalid='ignore'):
        w = transformed[:, 3:4]
        projected = np.where(w != 0, transformed[:, :3] / w, 0)
    return projected
