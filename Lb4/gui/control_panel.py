from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox

from Lb4.core.drawer import Drawer


class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._drawer = Drawer()
        self._iterations_validator = QIntValidator(1, 1_000_000)
        self._depth_validator = QIntValidator(1, 6)
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
        self._recursive_checkbox = QCheckBox("Использовать рекурсивную реализацию")
        self._depth_label = QLabel("Глубина рекурсии:")
        self._depth_input = QLineEdit("5")
        self._iterations_number_input.setValidator(self._iterations_validator)
        self._depth_input.setValidator(self._depth_validator)
        self._iterations_number_input.textChanged.connect(self.on_change)
        self._depth_input.textChanged.connect(self.on_change)
        self._color_checkbox.stateChanged.connect(self.on_change)
        self._recursive_checkbox.stateChanged.connect(self.on_change)

    def __layout_components(self):
        self._main_layout.addWidget(self._header_label)
        self._main_layout.addWidget(self._recursive_checkbox)
        self._main_layout.addWidget(self._iterations_number_label)
        self._main_layout.addWidget(self._iterations_number_input)
        self._main_layout.addWidget(self._color_checkbox)
        self._main_layout.addWidget(self._depth_label)
        self._main_layout.addWidget(self._depth_input)

    def paint(self):
        rec_flag = self._recursive_checkbox.isChecked()
        self._iterations_number_input.setDisabled(rec_flag)
        self._color_checkbox.setDisabled(rec_flag)
        self._depth_input.setEnabled(rec_flag)
        if rec_flag:
            depth = self._depth_input.text()
            self._drawer.paint_recursive(int(depth if depth != '' else 1))
        else:
            iterations_number = self._iterations_number_input.text()
            is_color_mode = self._color_checkbox.isChecked()
            self._drawer.paint(int(iterations_number if iterations_number != '' else 10), is_color_mode)

    def on_change(self):
        self._draw_area.update()

    def set_draw_area(self, draw_area):
        self._draw_area = draw_area
