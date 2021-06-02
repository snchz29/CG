import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QSlider, QCheckBox, QComboBox, QColorDialog, QPushButton


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


class ColorPicker(QPushButton):
    def __init__(self, label, drawarea):
        super().__init__(label)
        self.drawarea = drawarea
        self.color_dialog = QColorDialog()
        self.setFocusPolicy(Qt.NoFocus)
        self.clicked.connect(self.button_clicked)
        self.color_dialog.accepted.connect(self.color_accepted)

    def button_clicked(self):
        self.color_dialog.show()

    def color_accepted(self):
        color = self.color_dialog.currentColor().red(), \
                self.color_dialog.currentColor().green(), \
                self.color_dialog.currentColor().blue()
        logging.info(f"Choose color {color}")
        return color


class AmbientColorPicker(ColorPicker):
    def __init__(self, drawarea):
        super().__init__("Ambient", drawarea)

    def color_accepted(self):
        color = super().color_accepted()
        self.drawarea.set_ambient_color(*color)


class DiffuseColorPicker(ColorPicker):
    def __init__(self, drawarea):
        super().__init__("Diffuse", drawarea)

    def color_accepted(self):
        color = super().color_accepted()
        self.drawarea.set_diffuse_color(*color)


class SpecularColorPicker(ColorPicker):
    def __init__(self, drawarea):
        super().__init__("Specular", drawarea)

    def color_accepted(self):
        color = super().color_accepted()
        self.drawarea.set_specular_color(*color)


class ShininessCheckbox(QCheckBox):
    def __init__(self, drawarea):
        super().__init__("Включить отражение света")
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
        self._ambient_label = QLabel("Цвета источника света")
        self._main_layout.addWidget(self._ambient_label)
        self._ambient_color_picker = AmbientColorPicker(drawarea)
        self._diffuse_color_picker = DiffuseColorPicker(drawarea)
        self._specular_color_picker = SpecularColorPicker(drawarea)
        self._main_layout.addWidget(self._ambient_color_picker)
        self._main_layout.addWidget(self._diffuse_color_picker)
        self._main_layout.addWidget(self._specular_color_picker)
        self._shininess_checkbox = ShininessCheckbox(drawarea)
        self._main_layout.addWidget(self._shininess_checkbox)
        self._clipping_label = QLabel("Граница отсечения")
        self._clipping_slider = ClippingSlider(drawarea)
        self._main_layout.addWidget(self._clipping_label)
        self._main_layout.addWidget(self._clipping_slider)
        self._projection_label = QLabel("Вид проекции (ортог. или персп.)")
        self._projection_checkbox = ProjectionCheckbox(drawarea)
        self._main_layout.addWidget(self._projection_label)
        self._main_layout.addWidget(self._projection_checkbox)
