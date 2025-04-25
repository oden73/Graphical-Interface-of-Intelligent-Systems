from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel

from ui_components.toolbar import Toolbar
from ui_components.drawing_canvas import DrawingCanvas

# from curves.circle import Circle
# from curves.ellipse import Ellipse
# from curves.hyperbola import Hyperbola
# from curves.parabola import Parabola

from utils.debug_mode import StepDebugger


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Графический редактор кривых второго порядка')
        self.setGeometry(100, 100, 800, 600)

        self.toolbar: Toolbar = Toolbar()
        self.canvas: DrawingCanvas = DrawingCanvas()
        self.hint_label: QLabel = QLabel('Выберите первую точку фигуры')

        central_widget: QWidget = QWidget()
        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.hint_label)
        layout.addWidget(self.canvas)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.debugger = None
        self.toolbar.set_on_step_prev(self.step_back)
        self.toolbar.set_on_step_next(self.step_forward)
        self.toolbar.set_on_reset(self.reset_canvas)

        self.canvas.set_callback(self.build_from_clicks)
        self.canvas.set_hint_callback(self.hint_label.setText)
        self.toolbar.curve_selector.currentTextChanged.connect(self.canvas.set_curve_type)

    def step_forward(self):
        if self.debugger:
            self.canvas.set_points(self.debugger.next())

    def step_back(self):
        if self.debugger:
            self.canvas.set_points(self.debugger.prev())

    def build_from_clicks(self, curve):
        debug = self.toolbar.is_debug_mode()

        if debug:
            self.debugger = StepDebugger(curve.step_by_step())
            self.canvas.set_points(self.debugger.current())
            self.toolbar.enable_step_controls(True)
        else:
            self.canvas.set_points(curve.get_points())
            self.debugger = None
            self.toolbar.enable_step_controls(False)

    def reset_canvas(self):
        self.canvas.set_points([])
        self.canvas.clicked_points.clear()
        self.debugger = None
        self.toolbar.enable_step_controls(False)
        self.hint_label.setText("Выберите первую точку фигуры")
