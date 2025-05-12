from typing import Optional, List, Tuple
import numpy as np

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
from scipy.spatial import Delaunay, Voronoi, QhullError


class VoronoiDelaunayWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.points: List[Tuple[float, float]] = []
        self.tri: Optional[Delaunay] = None
        self.voronoi: Optional[Voronoi] = None
        self.setMinimumSize(800, 600)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.points.append((event.x(), event.y()))
            self.update_diagrams()
            self.update()

    def update_diagrams(self) -> None:
        if len(self.points) >= 3:
            points_np: np.ndarray = np.array(self.points)
            try:
                self.tri = Delaunay(points_np)
                self.voronoi = Voronoi(points_np)
            except QhullError:
                self.tri = None
                self.voronoi = None

    def paintEvent(self, event) -> None:
        painter: QPainter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.tri is not None:
            painter.setPen(QPen(Qt.black, 2))
            for simplex in self.tri.simplices:
                for i in range(3):
                    try:
                        p1_coords: np.ndarray = self.tri.points[simplex[i]]
                        p2_coords: np.ndarray = self.tri.points[simplex[(i + 1) % 3]]

                        if not (np.all(np.isfinite(p1_coords)) and np.all(np.isfinite(p2_coords))):
                            continue

                        p1_x, p1_y = int(p1_coords[0]), int(p1_coords[1])
                        p2_x, p2_y = int(p2_coords[0]), int(p2_coords[1])

                        if all(-10000 < c < 10000 for c in [p1_x, p1_y, p2_x, p2_y]):
                            painter.drawLine(QPoint(p1_x, p1_y), QPoint(p2_x, p2_y))

                    except (IndexError, ValueError, OverflowError):
                        continue

        if self.voronoi is not None:
            painter.setPen(QPen(Qt.red, 1))
            for ridge_points, ridge_vertices in zip(self.voronoi.ridge_points, self.voronoi.ridge_vertices):
                if -1 not in ridge_vertices:
                    v0: np.ndarray = self.voronoi.vertices[ridge_vertices[0]]
                    v1: np.ndarray = self.voronoi.vertices[ridge_vertices[1]]
                    if np.all(np.isfinite(v0)) and np.all(np.isfinite(v1)):
                        painter.drawLine(QPoint(int(v0[0]), int(v0[1])), QPoint(int(v1[0]), int(v1[1])))

        painter.setPen(QPen(Qt.blue, 5))
        for x, y in self.points:
            painter.drawPoint(int(x), int(y))
