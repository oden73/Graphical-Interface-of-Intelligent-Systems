from src.core.matrix import (
    multiply_matrix,
    multiply_vertex_matrix,
    create_translation_matrix,
    create_rotation_matrix,
    create_scaling_matrix,
    create_reflection_matrix
)


class Object3D:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.transformation = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

    def apply_transformation(self, matrix):
        self.transformation = multiply_matrix(matrix, self.transformation)

    def get_transformed_vertices(self):
        transformed = []
        for vertex in self.vertices:
            new_vertex = multiply_vertex_matrix(vertex, self.transformation)
            transformed.append(new_vertex)
        return transformed

    def reset_transformations(self):
        self.transformation = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

    @classmethod
    def create_from_file(cls, file_path):
        from src.utils.file_loader import FileLoader
        vertices, edges = FileLoader.load(file_path)
        return cls(vertices, edges)
