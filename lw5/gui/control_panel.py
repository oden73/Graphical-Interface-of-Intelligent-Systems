from typing import Callable
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class ControlPanel(QWidget):
    def __init__(self,
                 build_polygon_callback: Callable[[], None],
                 check_point_callback: Callable[[], None],
                 reset_callback: Callable[[], None]) -> None:
        super().__init__()

        self.layout: QVBoxLayout = QVBoxLayout()

        self.build_button: QPushButton = QPushButton('Построить полигон')
        self.check_button: QPushButton = QPushButton('Проверить точку')
        self.reset_button: QPushButton = QPushButton('Очистить')

        self.build_button.clicked.connect(build_polygon_callback)
        self.check_button.clicked.connect(check_point_callback)
        self.reset_button.clicked.connect(reset_callback)

        self.layout.addWidget(self.build_button)
        self.layout.addWidget(self.check_button)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)

