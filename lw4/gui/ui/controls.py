from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class ControlsPanel(QWidget):
    def __init__(self, renderer, obj, parent=None):
        super().__init__(parent)
        self.renderer = renderer
        self.obj = obj

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Управление проекцией:"))

        btn_perspective = QPushButton("Перспектива")
        btn_perspective.clicked.connect(self.set_perspective)
        layout.addWidget(btn_perspective)

        btn_orthographic = QPushButton("Ортографическая")
        btn_orthographic.clicked.connect(self.set_orthographic)
        layout.addWidget(btn_orthographic)

        layout.addSpacing(10)
        layout.addWidget(QLabel("Прочее:"))

        btn_reset = QPushButton("Сброс трансформаций")
        btn_reset.clicked.connect(self.reset_transformations)
        layout.addWidget(btn_reset)

        self.setLayout(layout)

    def set_perspective(self):
        self.renderer.set_projection('perspective')

    def set_orthographic(self):
        self.renderer.set_projection('orthographic')

    def reset_transformations(self):
        self.obj.reset_transformations()
        self.renderer.update()
