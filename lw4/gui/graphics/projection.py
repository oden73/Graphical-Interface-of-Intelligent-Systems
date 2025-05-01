import math


def create_perspective_matrix(fov, aspect, near, far):
    f = 1. / math.tan(math.radians(fov) / 2)
    return [
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * near * far) / (near - far)],
        [0, 0, -1, 0]
    ]
