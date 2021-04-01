import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QSlider


class WeightSlider(QSlider):
    def __init__(self, mediator):
        super().__init__(Qt.Horizontal)
        self.setFocusPolicy(Qt.NoFocus)
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
        self.setVisible(False)
        self._mediator = mediator
        self._mediator.register_info_widget(self)
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        self._point_name_label = QLabel()
        self._weight_value_label = QLabel()
        self._mediator.register_weight_value_label(self._weight_value_label)
        self._weight_slider = WeightSlider(mediator)
        self._mediator.register_weight_slider(self._weight_slider)
        self._main_layout.addWidget(self._point_name_label)
        self._main_layout.addWidget(self._weight_value_label)
        self._main_layout.addWidget(self._weight_slider)

    def set_point(self, point_idx):
        self._point_name_label.setText(f"Точка номер {point_idx + 1}")


class ControlPanel(QWidget):
    def __init__(self, mediator):
        super().__init__()
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        self._header_label = QLabel("Лабораторная работа № 3\nNURB-spline\n8382 Нечепуренко Н.А., Терехов А.Е.")
        self._instruction_label = QLabel("Для перемещения точек используйте\nWASD или стрелки.\n"
                                         "Для выбора точки нажмите на нее.\n"
                                         "Для перемещения между точками\nиспользуйте TAB.")
        self._point_info = PointInfoWidget(mediator)
        self._main_layout.addWidget(self._header_label)
        self._main_layout.addWidget(self._instruction_label)
        self._main_layout.addWidget(self._point_info)