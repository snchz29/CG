import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QSlider, QCheckBox, QColorDialog, QPushButton

TITLE = """Лабораторная работа № 7
Реализация трехмерного объекта
с использованием библиотеки OpenGL
8382 Нечепуренко Н.А., Терехов А.Е."""


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
    def __init__(self, drawarea, o, p):
        super().__init__("Включить ортог. проекцию")
        self._drawarea = drawarea
        self._o = o
        self._p = p
        self._o.setVisible(True)
        self._p.setVisible(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCheckState(2)
        self.stateChanged.connect(self.handler)

    def handler(self):
        self._drawarea.set_projection_state(self.checkState())
        if self.checkState() == 0:
            self._o.setVisible(False)
            self._p.setVisible(True)
        else:
            self._o.setVisible(True)
            self._p.setVisible(False)

        logging.info(f"Projection checkbox value has changed to {self.checkState()}")


class OrthoSliders(QWidget):
    def __init__(self, drawarea):
        super().__init__()
        self._drawarea = drawarea
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self._x_slider = QSlider(Qt.Horizontal)
        self._x_slider.setMinimum(20)
        self._x_slider.setMaximum(200)
        self._x_slider.setValue(200)
        self._y_slider = QSlider(Qt.Horizontal)
        self._y_slider.setMinimum(20)
        self._y_slider.setMaximum(200)
        self._y_slider.setValue(200)
        self._z_slider = QSlider(Qt.Horizontal)
        self._z_slider.setMinimum(20)
        self._z_slider.setMaximum(200)
        self._z_slider.setValue(200)
        self._x_label = QLabel("X:")
        self._y_label = QLabel("Y:")
        self._z_label = QLabel("Z:")

        self._layout.addWidget(self._x_label)
        self._layout.addWidget(self._x_slider)

        self._layout.addWidget(self._y_label)
        self._layout.addWidget(self._y_slider)

        self._layout.addWidget(self._z_label)
        self._layout.addWidget(self._z_slider)

        self._x_slider.valueChanged.connect(self._handle_x)
        self._y_slider.valueChanged.connect(self._handle_y)
        self._z_slider.valueChanged.connect(self._handle_z)

    def _handle_x(self):
        self._drawarea.set_x_ortho(self._x_slider.value() / 100)

    def _handle_y(self):
        self._drawarea.set_y_ortho(self._y_slider.value() / 100)

    def _handle_z(self):
        self._drawarea.set_z_ortho(self._z_slider.value() / 100)


class ProjectSliders(QWidget):
    def __init__(self, drawarea):
        super().__init__()
        self._drawarea = drawarea
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self._fov_label = QLabel("FOV: ")
        self._fov_slider = QSlider(Qt.Horizontal)
        self._fov_slider.setValue(90)
        self._fov_slider.setMaximum(90)
        self._fov_slider.setMinimum(45)
        self._layout.addWidget(self._fov_label)
        self._layout.addWidget(self._fov_slider)
        self._fov_slider.valueChanged.connect(self._fov_handler)

    def _fov_handler(self):
        self._drawarea.set_fov(self._fov_slider.value())


class ControlPanel(QWidget):
    def __init__(self, drawarea):
        super().__init__()
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        self._header_label = QLabel(TITLE)
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
        self._ortho_controls = OrthoSliders(drawarea)
        self._proj_controls = ProjectSliders(drawarea)
        self._projection_checkbox = ProjectionCheckbox(drawarea, self._ortho_controls, self._proj_controls)
        self._main_layout.addWidget(self._projection_label)
        self._main_layout.addWidget(self._projection_checkbox)
        self._main_layout.addWidget(self._ortho_controls)
        self._main_layout.addWidget(self._proj_controls)
