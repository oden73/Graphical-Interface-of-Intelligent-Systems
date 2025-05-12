from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
)

from voronoi_delaunay_widget import VoronoiDelaunayWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Диаграмма Вороного и триангуляция Делоне')
        self.widget: VoronoiDelaunayWidget = VoronoiDelaunayWidget()

        clear_button: QPushButton = QPushButton('Очистить')
        clear_button.clicked.connect(self.clear)

        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(self.widget)
        layout.addWidget(clear_button)

        container: QWidget = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def clear(self) -> None:
        self.widget.points.clear()
        self.widget.tri = None
        self.widget.voronoi = None
        self.widget.update()
