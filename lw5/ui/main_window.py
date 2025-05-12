from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QApplication
from PyQt5.QtCore import Qt, QPointF
from typing import List, Tuple

from ui.canvas import Canvas

from algorithms.graham import graham_scan
from algorithms.jarvis import jarvis_march

from geometry.convexity_checker import is_convex
from geometry.internal_normals import compute_internal_normals
from geometry.intersections import find_segment_polygon_intersection
from geometry.point_in_polygon import is_point_inside_polygon

from models.polygon import Polygon


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Графический редактор')
        self.resize(800, 600)

        self.canvas: Canvas = Canvas()
        self.setCentralWidget(self.canvas)

        self.init_toolbar()

    def init_toolbar(self) -> None:
        toolbar: QToolBar = QToolBar('Построение полигона')
        toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        clear_action: QAction = QAction('Очистить', self)
        clear_action.triggered.connect(self.canvas.clear)
        toolbar.addAction(clear_action)

        convex_action: QAction = QAction('Проверить выпуклость', self)
        convex_action.triggered.connect(self.check_convex)
        toolbar.addAction(convex_action)

        normals_action: QAction = QAction('Построить нормали', self)
        normals_action.triggered.connect(self.build_normals)
        toolbar.addAction(normals_action)

        graham_action: QAction = QAction('Оболочка (Грэхем)', self)
        graham_action.triggered.connect(self.build_graham)
        toolbar.addAction(graham_action)

        jarvis_action: QAction = QAction('Оболочка (Джарвис)', self)
        jarvis_action.triggered.connect(self.build_jarvis)
        toolbar.addAction(jarvis_action)

        enter_segment_mode_action: QAction = QAction('Задать отрезок', self)
        enter_segment_mode_action.triggered.connect(self.canvas.enter_segment_mode)
        toolbar.addAction(enter_segment_mode_action)

        segment_action: QAction = QAction('Найти пересечения', self)
        segment_action.triggered.connect(self.check_intersections)
        toolbar.addAction(segment_action)

        enter_point_mode_action: QAction = QAction('Задать точку', self)
        enter_point_mode_action.triggered.connect(self.canvas.enter_point_mode)
        toolbar.addAction(enter_point_mode_action)

        point_action: QAction = QAction('Проверка точки', self)
        point_action.triggered.connect(self.check_point)
        toolbar.addAction(point_action)

        reset_normals_action = QAction("Сбросить нормали", self)
        reset_normals_action.triggered.connect(self.canvas.reset_normals)
        toolbar.addAction(reset_normals_action)

        reset_hull_action = QAction("Сбросить оболочку", self)
        reset_hull_action.triggered.connect(self.canvas.reset_convex_hull)
        toolbar.addAction(reset_hull_action)

        reset_segment_action = QAction("Сбросить отрезок", self)
        reset_segment_action.triggered.connect(self.canvas.reset_segment)
        toolbar.addAction(reset_segment_action)

        reset_point_action = QAction("Сбросить точку", self)
        reset_point_action.triggered.connect(self.canvas.reset_test_point)
        toolbar.addAction(reset_point_action)

    def check_convex(self) -> None:
        if is_convex(self.canvas.polygon.points):
            self.canvas.set_message('Полигон выпуклый')
        else:
            self.canvas.set_message('Полигон НЕ выпуклый')
        self.canvas.update()

    def build_normals(self) -> None:
        normals: List[Tuple[Tuple[int, int], Tuple[float, float]]] = compute_internal_normals(self.canvas.polygon.points)
        self.canvas.normals = normals
        self.canvas.update()

    def build_graham(self) -> None:
        hull: List[QPointF] = graham_scan(self.canvas.polygon.points)
        self.canvas.convex_hull = Polygon(hull)
        self.canvas.update()

    def build_jarvis(self) -> None:
        hull: List[QPointF] = jarvis_march(self.canvas.polygon.points)
        self.canvas.convex_hull = Polygon(hull)
        self.canvas.update()

    def check_intersections(self) -> None:
        if not self.canvas.test_segment:
            self.canvas.set_message('Отрезок не задан')
            return

        intersections: List[QPointF] = find_segment_polygon_intersection(
            self.canvas.test_segment.start, self.canvas.test_segment.end, self.canvas.polygon.points
        )
        self.canvas.intersections = [(i.x(), i.y()) for i in intersections]
        self.canvas.set_message('Точки пересечения нанесены на полигон')
        self.canvas.update()

    def check_point(self) -> None:
        if not self.canvas.test_point:
            self.canvas.set_message('Точка не задана')
            return

        inside: bool = is_point_inside_polygon(
            QPointF(float(self.canvas.test_point[0]), float(self.canvas.test_point[1])),
            self.canvas.polygon.points)
        if inside:
            self.canvas.set_message('Точка ВНУТРИ полигона')
        else:
            self.canvas.set_message('Точка СНАРУЖИ полигона')
        self.canvas.update()
