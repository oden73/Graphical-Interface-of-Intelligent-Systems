from typing import Optional
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSlot

from gui.canvas_widget import CanvasWidget
from gui.control_panel import ControlPanel


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Предварительная обработка полигонов')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget: QWidget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout: QVBoxLayout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.canvas: CanvasWidget = CanvasWidget()
        self.layout.addWidget(self.canvas)

        self.control_panel: ControlPanel = ControlPanel(
            self.build_polygon, self.check_point, self.reset_canvas
        )
        self.layout.addWidget(self.control_panel)

    @pyqtSlot()
    def build_polygon(self) -> None:
        self.canvas.build_polygon()

    @pyqtSlot()
    def check_point(self) -> None:
        self.canvas.check_point_inside()

    @pyqtSlot()
    def reset_canvas(self) -> None:
        self.canvas.clear_canvas()
