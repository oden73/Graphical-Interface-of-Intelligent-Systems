from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction
from gui.viewer3d import Viewer3D


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Графический редактор 3D объектов')
        self.resize(800, 600)

        self.viewer: Viewer3D = Viewer3D(self)
        self.setCentralWidget(self.viewer)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("&Файл")

        open_action = QAction("&Открыть", self)
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        self.viewer.setFocus()

    def _open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Открыть модель", "", "Text Files (*.txt)")
        if path:
            self.viewer.load_model(path)
