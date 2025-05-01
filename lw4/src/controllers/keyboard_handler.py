from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsView

from src.core.matrix import (
    create_translation_matrix,
    create_rotation_matrix,
    create_scaling_matrix,
    create_reflection_matrix,
    create_perspective_matrix
)
from src.core.object_3d import Object3D


class KeyboardHandler:
    def __init__(self, obj: Object3D, graphics_view: QGraphicsView) -> None:
        self.obj = obj
        self.graphics_view = graphics_view
        self.rotation_step = 5  # угол поворота в градусах
        self.translation_step = 0.1  # шаг перемещения
        self.scaling_step = 1.1  # коэф масштабирования

        self.key_actions = {
            Qt.Key_W: lambda: create_translation_matrix(0, self.translation_step, 0),
            Qt.Key_S: lambda: create_translation_matrix(0, -self.translation_step, 0),
            Qt.Key_A: lambda: create_translation_matrix(-self.translation_step, 0, 0),
            Qt.Key_D: lambda: create_translation_matrix(self.translation_step, 0, 0),
            Qt.Key_Q: lambda: create_rotation_matrix('y', self.rotation_step),
            Qt.Key_E: lambda: create_rotation_matrix('y', -self.rotation_step),
            Qt.Key_R: lambda: create_rotation_matrix('x', self.rotation_step),
            Qt.Key_F: lambda: create_rotation_matrix('x', -self.rotation_step),
            Qt.Key_T: lambda: create_rotation_matrix('z', self.rotation_step),
            Qt.Key_G: lambda: create_rotation_matrix('z', -self.rotation_step),
            Qt.Key_Plus: lambda: create_scaling_matrix(self.scaling_step, self.scaling_step, self.scaling_step),
            Qt.Key_Minus: lambda: create_scaling_matrix(1 / self.scaling_step, 1 / self.scaling_step, 1 / self.scaling_step),
            Qt.Key_X: lambda: create_reflection_matrix('x'),
            Qt.Key_Y: lambda: create_reflection_matrix('y'),
            Qt.Key_Z: lambda: create_reflection_matrix('z'),
            Qt.Key_P: self.apply_perspective
        }

    def handle_key(self, event):
        key = event.key()
        if key in self.key_actions:
            action = self.key_actions[key]
            if callable(action):
                matrix = action()
                self.obj.apply_transformation(matrix)
                self.graphics_view.update()

    @staticmethod
    def apply_perspective(self):
        fov = 45
        aspect = 16/9
        near, far = 0.1, 100
        perspective_matrix = create_perspective_matrix(fov, aspect, near, far)
        self.obj.apply_transformation(perspective_matrix)
