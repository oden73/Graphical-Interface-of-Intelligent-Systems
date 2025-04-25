from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtCore import Qt


class DebugOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.points = []
        self.tangents = []
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def set_debug_data(self, points, tangents=None):
        self.points = points
        self.tangents = tangents or []
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.red)
        pen.setWidth(2)
        painter.setPen(pen)

        for i, (x, y) in enumerate(self.points):
            painter.drawText(x + 5, y - 5, f'P{i + 1}')

        pen.setColor(Qt.blue)
        painter.setPen(pen)

        for (start, end) in self.tangents:
            painter.drawLine(start[0], start[1], end[0], end[1])
