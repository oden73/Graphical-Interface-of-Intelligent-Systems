from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QPointF, QPoint
from typing import List, Tuple, Callable, Optional

from graphics.bresenham import bresenham
from models.polygon import Polygon
from models.segment import Segment


class Canvas(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.polygon: Polygon = Polygon()
        self.convex_hull: Optional[Polygon] = None
        self.normals: List[Tuple[Tuple[int, int], Tuple[float, float]]] = []

        self.test_segment: Optional[Segment] = None
        self.test_point: Optional[Tuple[int, int]] = None
        self.intersections: List[Tuple[float, float]] = []

        self.mode: str = 'default'  # default, draw_segment, draw_point
        self.temp_segment_points: List[Tuple[int, int]] = []
        self.message: str = ''

    def clear(self) -> None:
        self.polygon = Polygon()
        self.convex_hull = None
        self.normals = []
        self.test_segment = None
        self.test_point = None
        self.intersections = []
        self.mode = 'default'
        self.temp_segment_points = []
        self.message = ''
        self.update()

    def set_message(self, msg: str) -> None:
        self.message = msg
        self.update()

    def reset_normals(self) -> None:
        self.normals = []
        self.update()

    def reset_convex_hull(self) -> None:
        self.convex_hull = None
        self.update()

    def reset_segment(self) -> None:
        self.test_segment = None
        self.intersections = []
        self.temp_segment_points = []
        self.mode = 'default'
        self.set_message('')
        self.update()

    def reset_test_point(self) -> None:
        self.test_point = None
        self.mode = 'default'
        self.set_message('')
        self.update()

    def enter_segment_mode(self) -> None:
        self.reset_segment()
        self.mode = 'draw_segment'
        self.set_message('Укажите 2 точки отрезка для проверки пересечений')

    def enter_point_mode(self) -> None:
        self.reset_test_point()
        self.mode = 'draw_point'
        self.set_message('Укажите точку для проверки принадлежности')

    def mousePressEvent(self, event) -> None:
        x, y = event.x(), event.y()

        if self.mode == 'draw_segment':
            self.temp_segment_points.append((x, y))
            if len(self.temp_segment_points) == 2:
                self.test_segment = Segment(
                    QPointF(float(self.temp_segment_points[0][0]), float(self.temp_segment_points[0][1])),
                    QPointF(float(self.temp_segment_points[1][0]), float(self.temp_segment_points[1][1]))
                )
                self.mode = 'default'
                self.set_message('Отрезок задан. Выполните проверку пересечений')
                self.update()
        elif self.mode == 'draw_point':
            self.test_point = (x, y)
            self.mode = 'default'
            self.set_message('Точка задана. Выполните проверку принадлежности')
            self.update()
        else:
            self.polygon.add_point(QPointF(x, y))
            self.update()

    def paintEvent(self, event) -> None:
        painter: QPainter = QPainter(self)
        pen: QPen = QPen(Qt.black, 2)
        painter.setPen(pen)

        points: List[QPointF] = self.polygon.points
        if len(points) > 1:
            for i in range(len(points)):
                start: QPointF = points[i]
                end: QPointF = points[(i + 1) % len(points)]
                painter.drawLine(start, end)

        if self.convex_hull:
            pen = QPen(Qt.blue, 2, Qt.DashLine)
            painter.setPen(pen)
            ch_points: List[QPointF] = self.convex_hull.points
            for i in range(len(ch_points)):
                start: QPointF = ch_points[i]
                end: QPointF = ch_points[(i + 1) % len(ch_points)]

                painter.drawLine(start, end)

        pen = QPen(Qt.darkGreen, 1)
        painter.setPen(pen)
        for (start, vec) in self.normals:
            end: Tuple[int, int] = (int(start[0] + vec[0] * 20), int(start[1] + vec[1] * 20))
            start_point = QPoint(int(start[0]), int(start[1]))
            end_point = QPoint(int(end[0]), int(end[1]))

            painter.drawLine(start_point, end_point)

        if self.test_segment:
            pen = QPen(Qt.red, 2)
            painter.setPen(pen)
            self._draw_line(painter, self.test_segment.start, self.test_segment.end)

            for point in self.intersections:
                painter.setBrush(Qt.red)
                painter.drawEllipse(QPoint(int(point[0]), int(point[1])), 4, 4)

        if self.test_point:
            pen = QPen(Qt.magenta, 2)
            painter.setPen(pen)
            painter.setBrush(Qt.magenta)
            painter.drawEllipse(QPoint(*self.test_point), 4, 4)

        if self.message != '':
            painter.setPen(QPen(Qt.darkBlue))
            painter.setFont(QFont('Arial', 14))
            painter.drawText(10, self.height() - 10, self.message)

    @staticmethod
    def _draw_line(painter: QPainter, p1: QPointF, p2: QPointF) -> None:
        for x, y in bresenham(int(p1.x()), int(p1.y()), int(p2.x()), int(p2.y())):
            painter.drawPoint(x, y)
