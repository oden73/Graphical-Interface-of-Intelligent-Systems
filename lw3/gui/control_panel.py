from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox


class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.label = QLabel('Выберите тип кривой:')
        self.curve_selector = QComboBox()
        self.curve_selector.addItems(['Hermite', 'Bezier', 'B-Spline'])

        self.reset_button = QPushButton('Reset')

        layout.addWidget(self.label)
        layout.addWidget(self.curve_selector)
        layout.addWidget(self.reset_button)
        layout.addStretch()

        self.setLayout(layout)
