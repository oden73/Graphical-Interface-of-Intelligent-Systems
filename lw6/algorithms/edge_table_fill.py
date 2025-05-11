import time

from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QApplication

from algorithms.base import FillAlgorithm


class EdgeTableScanlineFill(FillAlgorithm):
    def fill(self, polygon):
        if not polygon.closed:
            return

        edges = []
        points = polygon.points
        for i in range(len(points)):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % len(points)]
            if y0 == y1:
                continue  # игнорируем горизонтальные
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            edges.append({'y_min': y0, 'y_max': y1, 'x': x0, 'inv_slope': (x1 - x0) / (y1 - y0)})

        edges.sort(key=lambda e: (e['y_min'], e['x']))
        y = min(e['y_min'] for e in edges)
        y_max = max(e['y_max'] for e in edges)
        AET = []
        count = 0

        while y < y_max:
            for e in edges:
                if e['y_min'] == y:
                    AET.append(e)
            AET = [e for e in AET if e['y_max'] > y]
            AET.sort(key=lambda e: e['x'])

            for i in range(0, len(AET), 2):
                x_start = int(round(AET[i]['x']))
                x_end = int(round(AET[i+1]['x']))
                for x in range(x_start, x_end):
                    self.canvas.image.setPixel(x, y, QColor(0, 0, 255).rgb())

            if self.debug_mode:
                count += 1
                if count % 10 == 0:
                    self.canvas.setPixmap(QPixmap.fromImage(self.canvas.image))
                    QApplication.processEvents()
                    time.sleep(0.1)

            y += 1
            for e in AET:
                e['x'] += e['inv_slope']
