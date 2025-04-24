from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from ui_components.toolbar import Toolbar
from ui_components.drawing_canvas import DrawingCanvas

from curves.circle import Circle
from curves.ellipse import Ellipse
from curves.hyperbola import Hyperbola
from curves.parabola import Parabola

from utils.debug_mode import StepDebugger


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Графический редактор кривых второго порядка')
        self.setGeometry(100, 100, 800, 600)

        self.toolbar: Toolbar = Toolbar()
        self.canvas: DrawingCanvas = DrawingCanvas()

        central_widget: QWidget = QWidget()
        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.toolbar.set_on_generate(self.build_curve)

        self.debugger = None
        self.toolbar.set_on_generate(self.build_curve)
        self.toolbar.set_on_step_prev(self.step_back)
        self.toolbar.set_on_step_next(self.step_forward)

    def build_curve(self):
        curve_type: str = self.toolbar.get_selected_curve()
        debug: bool = self.toolbar.is_debug_mode()

        if curve_type == "Circle":
            curve = Circle(center_x=0, center_y=0, radius=10)
        elif curve_type == "Ellipse":
            curve = Ellipse(center_x=0, center_y=0, a=10, b=6)
        elif curve_type == "Hyperbola":
            curve = Hyperbola(center_x=0, center_y=0, a=6, b=4)
        elif curve_type == "Parabola":
            curve = Parabola(center_x=0, center_y=0, p=4)
        else:
            return

        if debug:
            self.debugger = StepDebugger(curve.step_by_step())
            self.canvas.set_points(self.debugger.current())
            self.toolbar.enable_step_controls(True)
        else:
            self.canvas.set_points(curve.get_points())
            self.debugger = None
            self.toolbar.enable_step_controls(False)

    def step_forward(self):
        if self.debugger:
            self.canvas.set_points(self.debugger.next())

    def step_back(self):
        if self.debugger:
            self.canvas.set_points(self.debugger.prev())
