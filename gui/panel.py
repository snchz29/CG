import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QSlider, QCheckBox, QComboBox


class PointsCountSlider(QSlider):
    def __init__(self, drawarea):
        super().__init__(Qt.Horizontal)
        self._drawarea = drawarea
        self.setFocusPolicy(Qt.NoFocus)
        self.setMinimum(8)
        self.setMaximum(20)
        self.setValue(8)
        self.valueChanged.connect(self.handler)

    def handler(self):
        self._drawarea.set_point_count(self.value())
        logging.info(f"Changed row points count to {self.value()}")


class AmbientList(QComboBox):
    def __init__(self, drawarea):
        super().__init__()
        self._drawarea = drawarea
        self.setFocusPolicy(Qt.NoFocus)
        self.addItem("Вариант 1")
        self.addItem("Вариант 2")
        self.addItem("Вариант 3")
        self.addItem("Вариант 4")
        self.currentIndexChanged.connect(self.handler)

    def handler(self):
        self._drawarea.set_ambient_type(self.currentIndex())
        logging.info(f"Changed ambient type to {self.currentText()} ({self.currentIndex()})")


class AmbientSlider(QSlider):
    def __init__(self, drawarea):
        super().__init__(Qt.Horizontal)
        self._drawarea = drawarea
        self.setFocusPolicy(Qt.NoFocus)
        self.setMinimum(-100)
        self.setMaximum(100)
        self.setValue(15)
        self.valueChanged.connect(self.handler)

    def handler(self):
        value = self.value() / 100
        self._drawarea.set_ambient(value)
        logging.info(f"Changed ambient value to {value}")


class ShininessCheckbox(QCheckBox):
    def __init__(self, drawarea):
        super().__init__("Включить блеск")
        self._drawarea = drawarea
        self.setFocusPolicy(Qt.NoFocus)
        self.stateChanged.connect(self.handler)

    def handler(self):
        self._drawarea.set_shininess_state(self.checkState())
        logging.info(f"Shininess checkbox value has changed to {self.checkState()}")


class ClippingSlider(QSlider):
    def __init__(self, drawarea):
        super().__init__(Qt.Horizontal)
        self._drawarea = drawarea
        self.setFocusPolicy(Qt.NoFocus)
        self.setMinimum(30)
        self.setMaximum(100)
        self.setValue(70)
        self.valueChanged.connect(self.handler)

    def handler(self):
        value = self.value() / 100
        self._drawarea.set_clipping_level(value)
        logging.info(f"Changed clipping value to {value}")


class AxisSlider(QSlider):
    def __init__(self, fn):
        super().__init__(Qt.Horizontal)
        self._fn = fn
        self.setFocusPolicy(Qt.NoFocus)
        self.setMinimum(50)
        self.setMaximum(120)
        self.setValue(90)
        self.valueChanged.connect(self.handler)

    def handler(self):
        value = self.value() / 100
        self._fn(value)
        logging.info(f"Set axis value to {value}")


class ProjectionCheckbox(QCheckBox):
    def __init__(self, drawarea):
        super().__init__("Включить ортог. проекцию")
        self._drawarea = drawarea
        self.setFocusPolicy(Qt.NoFocus)
        self.stateChanged.connect(self.handler)

    def handler(self):
        self._drawarea.set_projection_state(self.checkState())
        logging.info(f"Projection checkbox value has changed to {self.checkState()}")


class ControlPanel(QWidget):
    def __init__(self, drawarea):
        super().__init__()
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        self._header_label = QLabel("""
Лабораторная работа № 7
Реализация трехмерного объекта
с использованием библиотеки OpenGL
8382 Нечепуренко Н.А., Терехов А.Е.""")
        self._main_layout.addWidget(self._header_label)
        self._axis_label = QLabel("Параметры эллипсоида")
        self._axis_xslider = AxisSlider(drawarea.set_x_axis)
        self._axis_yslider = AxisSlider(drawarea.set_y_axis)
        self._axis_zslider = AxisSlider(drawarea.set_z_axis)
        self._main_layout.addWidget(self._axis_label)
        self._main_layout.addWidget(self._axis_xslider)
        self._main_layout.addWidget(self._axis_yslider)
        self._main_layout.addWidget(self._axis_zslider)
        self._points_count_label = QLabel("Мелкость разбиения")
        self._main_layout.addWidget(self._points_count_label)
        self._points_count_slider = PointsCountSlider(drawarea)
        self._main_layout.addWidget(self._points_count_slider)
        self._ambient_label = QLabel("Тип источника света")
        self._ambient_type = AmbientList(drawarea)
        self._main_layout.addWidget(self._ambient_label)
        self._main_layout.addWidget(self._ambient_type)
        self._ambient_label = QLabel("Интенсивность источника света")
        self._main_layout.addWidget(self._ambient_label)
        self._ambient_slider = AmbientSlider(drawarea)
        self._main_layout.addWidget(self._ambient_slider)
        self._shininess_label = QLabel("Вид проекции (ортог. или персп.)")
        self._shininess_checkbox = ShininessCheckbox(drawarea)
        self._main_layout.addWidget(self._shininess_label)
        self._main_layout.addWidget(self._shininess_checkbox)
        self._clipping_label = QLabel("Граница отсечения")
        self._clipping_slider = ClippingSlider(drawarea)
        self._main_layout.addWidget(self._clipping_label)
        self._main_layout.addWidget(self._clipping_slider)
        self._projection_label = QLabel("Вид проекции (ортог. или персп.)")
        self._projection_checkbox = ProjectionCheckbox(drawarea)
        self._main_layout.addWidget(self._projection_label)
        self._main_layout.addWidget(self._projection_checkbox)
