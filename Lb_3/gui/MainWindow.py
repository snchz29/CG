import logging

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt
from Lb_3.gui.drawarea import DrawArea


class WeightSlider(QSlider):
    def __init__(self, mediator):
        super().__init__(Qt.Horizontal)
        self._mediator = mediator
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(1)
        self.valueChanged.connect(self.handler)

    def handler(self):
        try:
            self._mediator.change_weight_value_label(self.value())
            self._mediator.change_current_point_weight(self.value())
            self._mediator.update()
        except Exception as e:
            logging.info(e)


class PointInfoWidget(QWidget):
    def __init__(self, mediator):
        super().__init__()
        self._mediator = mediator
        self._mediator.register_info_widget(self)
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        self._point_name_label = QLabel()
        self._weight_value_label = QLabel()
        self._mediator.register_weight_value_label(self._weight_value_label)
        self._weight_slider = WeightSlider(mediator)
        self._main_layout.addWidget(self._point_name_label)
        self._main_layout.addWidget(self._weight_value_label)
        self._main_layout.addWidget(self._weight_slider)


class ControlPanel(QWidget):
    def __init__(self, mediator):
        super().__init__()
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        self._header_label = QLabel("Лабораторная работа № 3\nNURB-spline\n8382 Нечепуренко Н.А., Терехов А.Е.")
        self._instruction_label = QLabel("Для перемещения точек используйте\nWASD или стрелки.")
        self._point_info = PointInfoWidget(mediator)
        self._main_layout.addWidget(self._header_label)
        self._main_layout.addWidget(self._instruction_label)
        self._main_layout.addWidget(self._point_info)


class Mediator:
    def __init__(self):
        self._weight_value_label = None
        self._point_info_widget = None
        self._drawer = None
        self._drawarea = None

    def register_info_widget(self, iw):
        self._point_info_widget = iw

    def register_weight_value_label(self, vl):
        self._weight_value_label = vl

    def register_drawer(self, drawer):
        self._drawer = drawer

    def register_drawarea(self, da):
        self._drawarea = da

    def change_weight_value_label(self, new_value):
        self._weight_value_label.setText(f"Вес точки: {new_value}")

    def change_current_point_weight(self, new_value):
        self._drawer.set_new_current_point_weight(new_value)

    def update(self):
        self._drawarea.update()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nechepurenko & Terekhov Ltd.")
        self._main_layout = QHBoxLayout()
        self.setLayout(self._main_layout)
        mediator = Mediator()
        self._draw_area = DrawArea(mediator)
        self._main_layout.addWidget(self._draw_area)
        self._control_panel = ControlPanel(mediator)
        self._main_layout.addWidget(self._control_panel)
        self.setMaximumSize(700, 480)
