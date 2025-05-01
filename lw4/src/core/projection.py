from src.core.matrix import multiply_matrix

import math


def create_perspective_matrix(fov, aspect, near, far):
    f = 1. / math.tan(math.radians(fov) / 2)
    return [
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * near * far) / (near - far)],
        [0, 0, -1, 0]
    ]


def create_orthographic_matrix(left, right, bottom, top, near, far):
    return [
        [2 / (right - left), 0, 0, -(right + left) / (right - left)],
        [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
        [0, 0, -2 / (far - near), -(far + near) / (far - near)],
        [0, 0, 0, 1]
    ]
