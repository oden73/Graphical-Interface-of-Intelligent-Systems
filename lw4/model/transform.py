import numpy as np


class TransformManager:
    def __init__(self) -> None:
        self.matrix: np.ndarray = np.identity(4)

    def reset(self) -> None:
        self.matrix = np.identity(4)

    def apply(self, transform_matrix: np.ndarray) -> None:
        self.matrix = self.matrix @ transform_matrix

    def get_matrix(self) -> np.ndarray:
        return self.matrix
