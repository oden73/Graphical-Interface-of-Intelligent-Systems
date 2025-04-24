from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt


def draw_grid(painter: QPainter, width: int, height: int, step: int):
    pen = QPen(QColor(220, 220, 220))
    pen.setStyle(Qt.DotLine)
    painter.setPen(pen)

    for x in range(0, width, step):
        painter.drawLine(x, 0, x, height)
    for y in range(0, height, step):
        painter.drawLine(0, y, width, y)

    pen = QPen(Qt.black)
    painter.setPen(pen)
    painter.drawLine(0, height // 2, width, height // 2)
    painter.drawLine(width // 2, 0, width // 2, height)
