from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox

from Lb5.core.drawer import Drawer


class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._drawer = Drawer()
        self._draw_area = None
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        self._main_layout.setAlignment(Qt.AlignTop)
        self.__initialize_components()
        self.__layout_components()

    def __initialize_components(self):
        self._header_label = QLabel(
            "Лабораторная работа № 5\nШейдеры\n8382 Нечепуренко Н.А., Терехов А.Е.")

    def __layout_components(self):
        self._main_layout.addWidget(self._header_label)

    def paint(self):
        pass

    def on_change(self):
        self._draw_area.update()

    def set_draw_area(self, draw_area):
        self._draw_area = draw_area