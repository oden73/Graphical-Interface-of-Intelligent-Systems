from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
import numpy as np

from model.object3d import Object3D
from model.transform import TransformManager
from utils import matrix_utils, projection


class Viewer3D(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.object3d: Object3D = Object3D()
        self.transform: TransformManager = TransformManager()
        self.projection_matrix: np.ndarray = projection.perspective_projection_matrix(d=3.)

    def load_model(self, path: str) -> None:
        self.object3d.load_from_file(path)
        self.update()

    def paintEvent(self, event) -> None:
        if self.object3d.vertices.size == 0:
            return

        painter: QPainter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen((QPen(Qt.black, 2)))

        center: QPoint = QPoint(self.width() // 2, self.height() // 2)
        edges: list[tuple[np.ndarray, np.ndarray]] = self.object3d.get_transformed_edges(
            self.transform.get_matrix() @ self.projection_matrix
        )

        for p1, p2 in edges:
            x1, y1 = int(p1[0] * 50 + center.x()), int(-p1[1] * 50 + center.y())
            x2, y2 = int(p2[0] * 50 + center.x()), int(-p2[1] * 50 + center.y())
            painter.drawLine(x1, y1, x2, y2)

    def keyPressEvent(self, event) -> None:
        key = event.key()
        t = None

        if key == Qt.Key_W:
            t = matrix_utils.translation_matrix(0, 0.1, 0)
        elif key == Qt.Key_S:
            t = matrix_utils.translation_matrix(0, -0.1, 0)
        elif key == Qt.Key_A:
            t = matrix_utils.translation_matrix(-0.1, 0, 0)
        elif key == Qt.Key_D:
            t = matrix_utils.translation_matrix(0.1, 0, 0)
        elif key == Qt.Key_Q:
            t = matrix_utils.translation_matrix(0, 0, 0.1)
        elif key == Qt.Key_E:
            t = matrix_utils.translation_matrix(0, 0, -0.1)

        elif key == Qt.Key_Left:
            t = matrix_utils.rotation_matrix_y(np.radians(-10))
        elif key == Qt.Key_Right:
            t = matrix_utils.rotation_matrix_y(np.radians(10))
        elif key == Qt.Key_Up:
            t = matrix_utils.rotation_matrix_x(np.radians(-10))
        elif key == Qt.Key_Down:
            t = matrix_utils.rotation_matrix_x(np.radians(10))

        elif key == Qt.Key_Plus or key == Qt.Key_Equal:
            t = matrix_utils.scale_matrix(1.1, 1.1, 1.1)
        elif key == Qt.Key_Minus or key == Qt.Key_Underscore:
            t = matrix_utils.scale_matrix(0.9, 0.9, 0.9)

        elif key == Qt.Key_Z:
            t = matrix_utils.reflection_matrix('xy')
        elif key == Qt.Key_X:
            t = matrix_utils.reflection_matrix('yz')
        elif key == Qt.Key_Y:
            t = matrix_utils.reflection_matrix('xz')

        elif key == Qt.Key_R:
            self.transform.reset()
            self.update()
            return

        if t is not None:
            self.transform.apply(t)
            self.update()
