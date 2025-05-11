import time
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QApplication

from algorithms.base import FillAlgorithm


class SimpleSeedFill(FillAlgorithm):
    def fill(self, polygon):
        if not polygon.closed or not polygon.points:
            return

        seed = polygon.points[0]
        target_color = QColor(255, 255, 255).rgb()
        fill_color = QColor(0, 255, 0).rgb()

        stack = [seed]
        count = 0
        while stack:
            x, y = stack.pop()
            if self.canvas.image.pixel(x, y) != target_color:
                continue
            self.canvas.image.setPixel(x, y, fill_color)
            stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

            if self.debug_mode:
                count += 1
                if count % 50 == 0:
                    self.canvas.setPixmap(QPixmap.fromImage(self.canvas.image))
                    QApplication.processEvents()
