from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

from curves.circle import Circle
from curves.ellipse import Ellipse
from curves.hyperbola import Hyperbola
from curves.parabola import Parabola


class DrawingCanvas(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.points = []
        self.grid_enabled = True
        self.scale = 10  # 1 логическая единица к 10 пикселям

        self.clicked_points = []
        self.curve_type = "Circle"
        self.on_curve_ready = None  # callback
        self.origin = (0, 0)

        self.hint_callback = None

    def set_hint_callback(self, callback):
        self.hint_callback = callback

    def set_points(self, points: list[tuple[int, int]]) -> None:
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

        # координатные оси
        pen = QPen(Qt.black)
        painter.setPen(pen)
        painter.drawLine(0, height // 2, width, height // 2)
        painter.drawLine(width // 2, 0, width // 2, height)

    def _draw_points(self, painter: QPainter):
        pen = QPen(Qt.red)
        pen.setWidth(2)
        painter.setPen(pen)

        cx, cy = self.width() // 2, self.height() // 2

        cell_size = self.scale
        for x, y in self.points:
            px = cx + x * self.scale
            py = cy - y * self.scale  # инверсия Y
            painter.fillRect(px - cell_size // 2, py - cell_size // 2, cell_size, cell_size, QColor(255, 0, 0))

    def set_curve_type(self, curve_type: str):
        self.curve_type = curve_type
        self.clicked_points.clear()

    def set_callback(self, callback):
        self.on_curve_ready = callback

    def mousePressEvent(self, event):
        cx, cy = self.width() // 2, self.height() // 2
        x = (event.x() - cx) // self.scale
        y = (cy - event.y()) // self.scale
        self.clicked_points.append((x, y))
        self._try_build_curve()

    def _try_build_curve(self):
        points = self.clicked_points

        if self.hint_callback:
            if self.curve_type == "Circle":
                self.hint_callback("Выберите точку на окружности")
            elif self.curve_type == "Ellipse":
                if len(self.clicked_points) == 1:
                    self.hint_callback("Выберите ось a")
                elif len(self.clicked_points) == 2:
                    self.hint_callback("Выберите ось b")
            elif self.curve_type == "Hyperbola":
                if len(self.clicked_points) == 1:
                    self.hint_callback("Выберите параметр a")
                elif len(self.clicked_points) == 2:
                    self.hint_callback("Выберите параметр b")
            elif self.curve_type == "Parabola":
                self.hint_callback("Выберите фокус (точку направления)")

        if self.curve_type == "Circle" and len(points) == 2:
            (x0, y0), (x1, y1) = points
            radius = int(((x1 - x0)**2 + (y1 - y0)**2)**0.5)
            self.on_curve_ready(Circle(x0, y0, radius))

            self.clicked_points.clear()
            if self.hint_callback:
                self.hint_callback("Выберите первую точку фигуры")

        elif self.curve_type == "Ellipse" and len(points) == 3:
            (x0, y0), (xa, ya), (xb, yb) = points
            a = abs(xa - x0)
            b = abs(yb - y0)
            self.on_curve_ready(Ellipse(x0, y0, a, b))

            self.clicked_points.clear()
            if self.hint_callback:
                self.hint_callback("Выберите первую точку фигуры")


        elif self.curve_type == "Hyperbola" and len(points) == 3:
            (x0, y0), (xa, ya), (xb, yb) = points
            a = abs(xa - x0)
            b = abs(yb - y0)
            self.on_curve_ready(Hyperbola(x0, y0, a, b))

            self.clicked_points.clear()
            if self.hint_callback:
                self.hint_callback("Выберите первую точку фигуры")

        elif self.curve_type == "Parabola" and len(points) == 2:
            (x0, y0), (xf, yf) = points
            p = int(((xf - x0)**2 + (yf - y0)**2)**0.5 / 2)
            self.on_curve_ready(Parabola(x0, y0, p))

            self.clicked_points.clear()
            if self.hint_callback:
                self.hint_callback("Выберите первую точку фигуры")
