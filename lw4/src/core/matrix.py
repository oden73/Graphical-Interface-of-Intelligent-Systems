import math


def multiply_matrix(a, b) -> list[list]:
    result = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i][j] += a[i][k] * b[k][j]

    return result


def multiply_vertex_matrix(vertex, matrix):
    x = (
        vertex[0] * matrix[0][0] +
        vertex[1] * matrix[1][0] +
        vertex[2] * matrix[2][0] +
        vertex[3] * matrix[3][0]
    )

    y = (
        vertex[0] * matrix[0][1] +
        vertex[1] * matrix[1][1] +
        vertex[2] * matrix[2][1] +
        vertex[3] * matrix[3][1]
    )

    z = (
        vertex[0] * matrix[0][2] +
        vertex[1] * matrix[1][2] +
        vertex[2] * matrix[2][2] +
        vertex[3] * matrix[3][2]
    )

    return x, y, z, 1.0


def create_translation_matrix(dx, dy, dz):
    return [
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ]


def create_rotation_matrix(axis, angle_degrees):
    angle_rad = math.radians(angle_degrees)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    if axis == 'x':
        return [
            [1, 0, 0, 0],
            [0, cos_a, -sin_a, 0],
            [0, sin_a, cos_a, 0],
            [0, 0, 0, 1]
        ]
    elif axis == 'y':
        return [
            [cos_a, 0, sin_a, 0],
            [0, 1, 0, 0],
            [-sin_a, 0, cos_a, 0],
            [0, 0, 0, 1]
        ]
    elif axis == 'z':
        return [
            [cos_a, -sin_a, 0, 0],
            [sin_a, cos_a, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]


def create_scaling_matrix(sx, sy, sz):
    return [
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ]


def create_reflection_matrix(axis):
    if axis == 'x':
        return [
            [-1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    elif axis == 'y':
        return [
            [1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    elif axis == 'z':
        return [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1]
        ]


def transpose_matrix(matrix):
    return [[matrix[i][j] for j in range(4)] for i in range(4)]

