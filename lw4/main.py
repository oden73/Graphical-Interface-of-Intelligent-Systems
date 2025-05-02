import sys
from PyQt5.QtWidgets import QApplication

from gui.ui.main_window import MainWindow
from src.core.object_3d import Object3D


def main():
    app = QApplication(sys.argv)

    object_file = 'assets/object.txt'
    object = Object3D.create_from_file(object_file)

    window = MainWindow(object)
    window.resize(1000, 700)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
