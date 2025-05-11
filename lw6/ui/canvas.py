from PyQt5 import QtCore, QtGui, QtWidgets

from model.polygon import Polygon
from algorithms.seed_fill import SimpleSeedFill
from algorithms.scanline_seed_fill import LineSeedFill


class Canvas(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QtGui.QImage(800, 600, QtGui.QImage.Format_RGB32)
        self.image.fill(QtCore.Qt.white)
        self.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.polygon = Polygon()
        self.current_algorithm = None
        self.debug_mode = False

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.polygon.add_point((event.x(), event.y()))
            self.update_polygon()
        elif event.button() == QtCore.Qt.RightButton:
            self.polygon.close()
            self.update_polygon()

    def update_polygon(self):
        self.image.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(self.image)
        pen = QtGui.QPen(QtCore.Qt.black)
        painter.setPen(pen)

        if len(self.polygon.points) > 1:
            for i in range(len(self.polygon.points) - 1):
                p1 = self.polygon.points[i]
                p2 = self.polygon.points[i + 1]
                painter.drawLine(*p1, *p2)
            if self.polygon.closed:
                painter.drawLine(*self.polygon.points[-1], *self.polygon.points[0])

        painter.end()
        self.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def fill_polygon(self):
        if not self.current_algorithm:
            print("[DEBUG] Алгоритм не выбран!")
            return

        print("[DEBUG] Запуск алгоритма заливки")

        if isinstance(self.current_algorithm, (SimpleSeedFill, LineSeedFill)):
            center = self.polygon.get_center()
            print(f"[DEBUG] Центр полигона: {center}")
            temp_polygon = Polygon()
            temp_polygon.points = [center] + self.polygon.points[1:]
            temp_polygon.closed = self.polygon.closed
            self.current_algorithm.fill(temp_polygon)
        else:
            self.current_algorithm.fill(self.polygon)

        self.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def set_algorithm(self, algorithm_class):
        self.current_algorithm = algorithm_class(self, self.debug_mode)

    def toggle_debug(self, enabled):
        self.debug_mode = enabled
        if self.current_algorithm:
            self.current_algorithm.debug_mode = enabled

    def clear(self):
        self.polygon.reset()
        self.image.fill(QtCore.Qt.white)
        self.setPixmap(QtGui.QPixmap.fromImage(self.image))
