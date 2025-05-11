from PyQt5 import QtWidgets, QtCore

from ui.canvas import Canvas
from algorithms.active_edge_fill import ActiveEdgeListFill
from algorithms.edge_table_fill import EdgeTableScanlineFill
from algorithms.seed_fill import SimpleSeedFill
from algorithms.scanline_seed_fill import LineSeedFill


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Графический редактор")
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)
        self.create_toolbar()
        self.create_menu()
        self.change_algorithm(0)

    def create_toolbar(self):
        toolbar = self.addToolBar("Инструменты")

        self.combo = QtWidgets.QComboBox()
        self.combo.addItems([
            "Сканлайн (таблица рёбер)",
            "Сканлайн (активные рёбра)",
            "Простая затравка",
            "Построчная затравка"
        ])
        self.combo.currentIndexChanged.connect(self.change_algorithm)
        toolbar.addWidget(self.combo)

        self.debug_checkbox = QtWidgets.QCheckBox("Отладка")
        self.debug_checkbox.stateChanged.connect(
            lambda state: self.canvas.toggle_debug(state == QtCore.Qt.Checked))
        toolbar.addWidget(self.debug_checkbox)

        fill_btn = QtWidgets.QPushButton("Заливка")
        fill_btn.clicked.connect(self.canvas.fill_polygon)
        toolbar.addWidget(fill_btn)

        clear_btn = QtWidgets.QPushButton("Очистить")
        clear_btn.clicked.connect(self.canvas.clear)
        toolbar.addWidget(clear_btn)

    def create_menu(self):
        menu = self.menuBar().addMenu("Алгоритмы")
        actions = [
            "Сканлайн (таблица рёбер)",
            "Сканлайн (активные рёбра)",
            "Простая затравка",
            "Построчная затравка"
        ]
        for i, name in enumerate(actions):
            action = QtWidgets.QAction(name, self)
            action.triggered.connect(lambda checked, idx=i: self.combo.setCurrentIndex(idx))
            menu.addAction(action)

    def change_algorithm(self, index):
        algos = [EdgeTableScanlineFill, ActiveEdgeListFill, SimpleSeedFill, LineSeedFill]
        self.canvas.set_algorithm(algos[index])
