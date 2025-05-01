from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from gui.graphics.gl_render import GLRenderer
from gui.ui.controls import ControlsPanel
from src.core.object_3d import Object3D
from src.controllers.keyboard_handler import KeyboardHandler


class MainWindow(QMainWindow):
    def __init__(self, object: Object3D):
        super().__init__()
        self.setWindowTitle('3D Трансформации')

        central_widget = QWidget()
        layout = QHBoxLayout()

        self.renderer: GLRenderer = GLRenderer()
        self.renderer.set_object(object)

        controls = ControlsPanel(self.renderer, object)

        self.keyboard_handler = KeyboardHandler(object, self.renderer)

        layout.addWidget(self.renderer, stretch=1)
        layout.addWidget(controls)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def keyPressEvent(self, event) -> None:
        self.keyboard_handler.handle_key(event)
