from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt


class DrawingCanvas(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.points = []
        self.grid_enabled = True
        self.scale = 10  # 1 логическая единица к 10 пикселям

    def get_points(self, points: list[tuple[int, int]]) -> None:
        self.points = points
        self.update()

    def toggle_grid(self, state: bool) -> None:
        self.grid_enabled = state
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self._draw_background(painter)
        self._draw_points(painter)

    def _draw_background(self, painter: QPainter):
        if not self.grid_enabled:
            return

        pen = QPen(QColor(220, 220, 220))
        pen.setStyle(Qt.DotLine)
        painter.setPen(pen)

        width, height = self.width(), self.height()
        step = self.scale

        for x in range(0, width, step):
            painter.drawLine(x, 0, x, height)
        for y in range(0, height, step):
            painter.drawLine(0, y, width, y)

        pen = QPen(Qt.black)
        painter.setPen(pen)
        painter.drawLine(0, height // 2, width, height // 2)
        painter.drawLine(width // 2, 0, width // 2, height)

    def _draw_points(self, painter: QPainter):
        pen = QPen(Qt.red)
        pen.setWidth(2)
        painter.setPen(pen)

        cx, cy = self.width() // 2, self.height() // 2

        for x, y in self.points:
            px = cx + x * self.scale
            py = cy - y * self.scale
            painter.drawLine(px, py)
