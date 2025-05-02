import numpy as np


def translation_matrix(dx, dy, dz) -> np.ndarray:
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ], dtype=float)


def scale_matrix(sx, sy, sz) -> np.ndarray:
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def rotation_matrix_x(theta) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def rotation_matrix_y(theta) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def rotation_matrix_z(theta) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def reflection_matrix(axis) -> np.ndarray:
    if axis == 'xy':
        return scale_matrix(1, 1, -1)
    elif axis == 'yz':
        return scale_matrix(-1, 1, 1)
    elif axis == 'xz':
        return scale_matrix(1, -1, 1)
    else:
        raise ValueError('Неверная координатная плоскость')


def compose_matrices(*matrices) -> np.ndarray:
    result = np.identity(4)
    for m in reversed(matrices):
        result = result @ m
    return result
