from typing import List, Optional
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QMouseEvent
from PyQt5.QtCore import Qt

from models.point import Point
from models.polygon import Polygon
from algorithms.point_in_polygon import is_point_in_polygon


class CanvasWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.points: List[Point] = []
        self.polygon: Optional[Polygon] = None
        self.test_point: Optional[Point] = None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        x: float = event.x()
        y: float = event.y()
        new_point: Point = Point(x, y)
        if self.polygon is None:
            self.points.append(new_point)
        else:
            self.test_point = new_point
        self.update()

    def paintEvent(self, event) -> None:
        painter: QPainter = QPainter(self)
        pen: QPen = QPen(Qt.black, 2)
        painter.setPen(pen)

        for point in self.points:
            painter.drawEllipse(int(point.x) - 2, int(point.y) - 2, 4, 4)

        if self.polygon is not None:
            for i in range(len(self.polygon.points)):
                start_point: Point = self.points[i]
                end_point: Point = self.points[(i + 1) % len(self.polygon.points)]
                painter.drawLine(
                    int(start_point.x), int(start_point.y),
                    int(end_point.x), int(end_point.y)
                )

        if self.test_point is not None:
            pen.setColor(Qt.red)
            painter.setPen(pen)
            painter.drawEllipse(int(self.test_point.x) - 3, int(self.test_point.y) - 3, 6, 6)

    def build_polygon(self) -> None:
        if len(self.points) < 3:
            QMessageBox.warning(self, 'Ошибка', 'Для построения полигона нужно минимум 3 точки.')
            return

        self.polygon = Polygon(self.points.copy())
        self.update()

    def check_point_inside(self) -> None:
        if self.polygon is None or self.test_point is None:
            QMessageBox.warning(self, 'Ошибка', 'Постройте полигон и укажите точку.')
            return

        is_inside: bool = is_point_in_polygon(self.test_point, self.polygon)
        message: str = 'Точка внутри полигона' if is_inside else 'Точка снаружи полигона'
        QMessageBox.information(self, 'Результат', message)

    def clear_canvas(self) -> None:
        self.points.clear()
        self.polygon = None
        self.test_point = None
        self.update()
