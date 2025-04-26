from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QCheckBox

from gui.debug_overlay import DebugOverlay
from gui.drawing_canvas import DrawingCanvas
from gui.control_panel import ControlPanel

from src.curves.bezier import BezierCurve
from src.curves.bspline import BSplineCurve
from src.curves.hermite import HermiteCurve


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Интерполяция и аппроксимация кривых')
        self.setMinimumSize(800, 600)

        self.canvas = DrawingCanvas()
        self.overlay = DebugOverlay(self.canvas)
        self.control_panel = ControlPanel()

        self.canvas.debug_overlay = self.overlay
        self.canvas.mouseMoveEvent = self.wrap_mouse_move(self.canvas.mouseMoveEvent)
        self.canvas.mouseReleaseEvent = self.wrap_mouse_release(self.canvas.mouseReleaseEvent)

        self.step_checkbox = QCheckBox('Debug')
        self.step_checkbox.stateChanged.connect(self.toggle_step_mode)

        container = QWidget()
        canvas_layout = QVBoxLayout()
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        canvas_layout.addWidget(self.canvas)
        canvas_layout.addWidget(self.overlay)

        canvas_frame = QWidget()
        canvas_frame.setLayout(canvas_layout)

        control_layout = QVBoxLayout()
        control_layout.addWidget(self.control_panel)
        control_layout.addWidget(self.step_checkbox)
        control_layout.addStretch()

        main_layout = QHBoxLayout()
        main_layout.addLayout(control_layout, 1)
        main_layout.addWidget(canvas_frame, 4)

        wrapper = QWidget()
        wrapper.setLayout(main_layout)
        self.setCentralWidget(wrapper)

        self.control_panel.reset_button.clicked.connect(self.canvas.clear)
        self.control_panel.curve_selector.currentTextChanged.connect(self.try_build_curve)
        self.canvas.mousePressEvent = self.wrap_mouse_click(self.canvas.mousePressEvent)

    def toggle_step_mode(self, state):
        self.canvas.step_by_step_enabled = (state == 2)

    def wrap_mouse_click(self, original_handler):
        def wrapped(event):
            original_handler(event)
            self.try_build_curve()
        return wrapped

    def wrap_mouse_move(self, original_handler):
        def wrapped(event):
            original_handler(event)
            if self.canvas.selected_point_index is not None:
                self.try_build_curve()
        return wrapped

    def wrap_mouse_release(self, original_handler):
        def wrapped(event):
            original_handler(event)
            self.try_build_curve()
        return wrapped

    def try_build_curve(self):
        points = self.canvas.control_points
        curve_type = self.control_panel.curve_selector.currentText()

        curve = None
        try:
            if curve_type == 'Hermite':
                if len(points) >= 2:
                    curve = HermiteCurve(points)
            elif curve_type == 'Bezier':
                if len(points) >= 2:
                    curve = BezierCurve(points)
            elif curve_type == 'B-Spline':
                if len(points) >= 4:
                    curve = BSplineCurve(points)
        except Exception as e:
            print(f'Ошибка: {e}')
            return

        if curve:
            try:
                curve_points = curve.get_points(200)
                self.canvas.set_curve_points(curve_points, animate=self.canvas.step_by_step_enabled)
            except Exception as e:
                print(f'Ошибка при построении кривой: {e}')
