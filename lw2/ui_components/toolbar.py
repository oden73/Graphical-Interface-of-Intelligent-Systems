from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox, QCheckBox


class Toolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.curve_selector = QComboBox()
        self.curve_selector.addItems(['Circle', 'Ellipse', 'Hyperbola', 'Parabola'])
        self.layout.addWidget(self.curve_selector)

        self.debug_mode_checkbox = QCheckBox('Debug')
        self.layout.addWidget(self.debug_mode_checkbox)

        self.prev_button = QPushButton("<-")
        self.prev_button.setEnabled(False)
        self.layout.addWidget(self.prev_button)

        self.next_button = QPushButton("->")
        self.next_button.setEnabled(False)
        self.layout.addWidget(self.next_button)

        self.reset_button = QPushButton("Reset")
        self.layout.addWidget(self.reset_button)

    def get_selected_curve(self) -> str:
        return self.curve_selector.currentText()

    def is_debug_mode(self) -> bool:
        return self.debug_mode_checkbox.isChecked()

    def set_on_step_prev(self, callback):
        self.prev_button.clicked.connect(callback)

    def set_on_step_next(self, callback):
        self.next_button.clicked.connect(callback)

    def set_on_reset(self, callback):
        self.reset_button.clicked.connect(callback)

    def enable_step_controls(self, enabled: bool):
        self.prev_button.setEnabled(enabled)
        self.next_button.setEnabled(enabled)
