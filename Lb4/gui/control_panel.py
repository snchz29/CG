from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox

from Lb4.core.drawer import Drawer


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
            "Лабораторная работа № 4\nIFS фрактал \"Ветка\"\n8382 Нечепуренко Н.А., Терехов А.Е.")
        self._iterations_number_label = QLabel("Число точек:")
        self._iterations_number_input = QLineEdit("10000")
        self._color_checkbox = QCheckBox("Использовать цветовую схему")
        self._iterations_number_input.textChanged.connect(self.on_change)
        self._color_checkbox.stateChanged.connect(self.on_change)

    def __layout_components(self):
        self._main_layout.addWidget(self._header_label)
        self._main_layout.addWidget(self._iterations_number_label)
        self._main_layout.addWidget(self._iterations_number_input)
        self._main_layout.addWidget(self._color_checkbox)

    def paint(self):
        iterations_number = self.__try_get_iteration_number()
        is_color_mode = self._color_checkbox.isChecked()
        self._drawer.paint(iterations_number, is_color_mode)

    def on_change(self):
        self._draw_area.update()

    def set_draw_area(self, draw_area):
        self._draw_area = draw_area

    def __try_get_iteration_number(self):
        try:
            number = int(self._iterations_number_input.text())
        except:
            pass
        else:
            return number
        return 10000
