import numpy as np


class Object3D:
    def __init__(self) -> None:
        self.vertices: np.ndarray = np.empty((0, 4), dtype=float)
        self.edges: list[tuple[int, int]] = []

    def load_from_file(self, filename) -> None:
        vertices = []
        edges = []
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if not parts:
                    continue
                if parts[0] == 'v':
                    x, y, z = map(float, parts[1:4])
                    vertices.append([x, y, z, 1.])
                elif parts[0] == 'e':
                    i, j = map(int, parts[1:3])
                    edges.append((i, j))

        self.vertices = np.array(vertices, dtype=float)
        self.edges = edges

    def get_transformed_edges(self, matrix: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
        transformed = self.vertices @ matrix.T
        projected = transformed[:, :3] / transformed[:, 3:4]
        return [(projected[i], projected[j]) for i, j in self.edges]
