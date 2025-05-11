import time

from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QApplication

from algorithms.base import FillAlgorithm


class LineSeedFill(FillAlgorithm):
    def fill(self, polygon):
        if not polygon.closed or not polygon.points:
            return

        seed = polygon.points[0]
        target_color = QColor(255, 255, 255).rgb()
        fill_color = QColor(255, 255, 0).rgb()

        stack = [seed]
        count = 0
        while stack:
            x, y = stack.pop()
            if self.canvas.image.pixel(x, y) != target_color:
                continue

            x_left = x
            while x_left > 0 and self.canvas.image.pixel(x_left - 1, y) == target_color:
                x_left -= 1
            x_right = x
            while x_right < self.canvas.image.width() - 1 and self.canvas.image.pixel(x_right + 1, y) == target_color:
                x_right += 1

            for xi in range(x_left, x_right + 1):
                self.canvas.image.setPixel(xi, y, fill_color)

            for nx in range(x_left, x_right + 1):
                for ny in [y - 1, y + 1]:
                    if 0 <= ny < self.canvas.image.height() and self.canvas.image.pixel(nx, ny) == target_color:
                        stack.append((nx, ny))

            if self.debug_mode:
                count += 1
                if count % 50 == 0:
                    self.canvas.setPixmap(QPixmap.fromImage(self.canvas.image))
                    QApplication.processEvents()
                    time.sleep(0.1)
