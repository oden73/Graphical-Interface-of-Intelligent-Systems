from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPointF, QTimer


class DrawingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.control_points = []
        self.curve_points = []
        self.draw_cells = True
        self.debug_overlay = None

        self.step_by_step_enabled = False
        self.current_step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._step_forward)

        self.selected_point_index = None
        self.selection_radius = 10

    def start_animation(self, interval=10):
        if not self.curve_points:
            return
        self.current_step = 0
        self.timer.start(interval)

    def _step_forward(self):
        self.current_step += 1
        if self.current_step >= len(self.curve_points):
            self.timer.stop()
        self.update()

    def set_curve_points(self, points, animate=False, interval=10):
        self.curve_points = points

        if animate and self.step_by_step_enabled:
            self.start_animation(interval)
        else:
            self.current_step = len(points)
            self.update()

    def clear(self):
        self.control_points = []
        self.curve_points = []
        if self.debug_overlay:
            self.debug_overlay.set_debug_data([])
        self.update()

    def mousePressEvent(self, event):
        pos = (event.x(), event.y())

        for i, (px, py) in enumerate(self.control_points):
            if (px - pos[0]) ** 2 + (py - pos[1]) ** 2 <= self.selection_radius ** 2:
                self.selected_point_index = i
                return

        self.control_points.append(pos)
        self.update()

    def mouseMoveEvent(self, event):
        if self.selected_point_index is not None:
            self.control_points[self.selected_point_index] = (event.x(), event.y())
            self.update()

    def mouseReleaseEvent(self, event):
        self.selected_point_index = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.draw_cells:
            painter.setPen(QPen(QColor(220, 220, 220), 1))
            grid_size = 20
            for x in range(0, self.width(), grid_size):
                painter.drawLine(x, 0, x, self.height())
            for y in range(0, self.height(), grid_size):
                painter.drawLine(0, y, self.width(), y)

        painter.setPen(QPen(Qt.black, 5))
        for x, y in self.control_points:
            painter.drawPoint(QPointF(x, y))

        if self.curve_points:
            painter.setPen(QPen(Qt.darkGreen, 2))
            visible_points = self.curve_points[:self.current_step]
            for i in range(len(visible_points) - 1):
                x1, y1 = visible_points[i]
                x2, y2 = visible_points[i + 1]
                painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        if self.debug_overlay:
            self.debug_overlay.set_debug_data(self.control_points)
