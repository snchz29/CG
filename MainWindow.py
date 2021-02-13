from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5 import QtCore, QtWidgets
from GLWidget import GLWidget

MAX_SLIDER_VALUE = 100


def scissor(fn):
    def wrapper(self):
        fn(self)
        self.label_x1_value.setText(str(round(self.scissor_range_x1.value() / MAX_SLIDER_VALUE, 2)))
        self.label_y1_value.setText(str(round(self.scissor_range_y1.value() / MAX_SLIDER_VALUE, 2)))
        self.label_x2_value.setText(str(round(self.scissor_range_x2.value() / MAX_SLIDER_VALUE, 2)))
        self.label_y2_value.setText(str(round(self.scissor_range_y2.value() / MAX_SLIDER_VALUE, 2)))
        self.widget.scissor(self.scissor_range_x1.value() / MAX_SLIDER_VALUE,
                            self.scissor_range_y1.value() / MAX_SLIDER_VALUE,
                            self.scissor_range_x2.value() / MAX_SLIDER_VALUE,
                            self.scissor_range_y2.value() / MAX_SLIDER_VALUE)
    return wrapper


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = GLWidget()
        self.setWindowTitle("Terekhov 8382 LR 1 & 2")
        self.label_x1_value = QtWidgets.QLabel("0")
        self.label_y1_value = QtWidgets.QLabel("1.0")
        self.label_x2_value = QtWidgets.QLabel("0")
        self.label_y2_value = QtWidgets.QLabel("1.0")

        self.line_edit_n_points = QtWidgets.QLineEdit()
        self.line_edit_n_points.setValidator(QIntValidator())
        self.line_edit_n_points.textChanged.connect(self.update_n_figures)
        self.line_edit_n_points.setText('5')
        self.check_box_presets = QtWidgets.QCheckBox("Use presets", self)
        self.check_box_presets.stateChanged.connect(self.update_checkbox)
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.widget)
        config_layout = QtWidgets.QVBoxLayout()

        self.init_combo_box_figures()

        config_layout.addWidget(QtWidgets.QLabel("LAB 1"))
        config_layout.addWidget(QtWidgets.QLabel("Figure"))
        config_layout.addWidget(self.combo_box_figure)
        config_layout.addWidget(QtWidgets.QLabel("Quantity of figures"))

        count_layout = QtWidgets.QHBoxLayout()
        count_layout.addWidget(self.line_edit_n_points)
        count_layout.addWidget(self.check_box_presets)
        config_layout.addLayout(count_layout)
        config_layout.addWidget(QtWidgets.QLabel("LAB 2"))
        config_layout.addWidget(QtWidgets.QLabel("Scissor test"))

        self.init_scissor_utils()

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(QtWidgets.QLabel("X1"), 1, 0)
        grid_layout.addWidget(self.scissor_range_x1, 1, 1)
        grid_layout.addWidget(self.label_x1_value, 1, 2)
        grid_layout.addWidget(QtWidgets.QLabel("X2"), 2, 0)
        grid_layout.addWidget(self.scissor_range_x2, 2, 1)
        grid_layout.addWidget(self.label_x2_value, 2, 2)
        grid_layout.addWidget(QtWidgets.QLabel("Y1"), 3, 0)
        grid_layout.addWidget(self.scissor_range_y1, 3, 1)
        grid_layout.addWidget(self.label_y1_value, 3, 2)
        grid_layout.addWidget(QtWidgets.QLabel("Y2"), 4, 0)
        grid_layout.addWidget(self.scissor_range_y2, 4, 1)
        grid_layout.addWidget(self.label_y2_value, 4, 2)

        config_layout.addLayout(grid_layout)

        self.init_combo_box_alpha()

        self.slider_alpha = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_alpha.setRange(0, MAX_SLIDER_VALUE)
        self.slider_alpha.setValue(MAX_SLIDER_VALUE)
        self.slider_alpha.valueChanged.connect(self.update_alpha_value)
        config_layout.addWidget(QtWidgets.QLabel("Alpha test"))
        config_layout.addWidget(self.combo_box_alpha)
        config_layout.addWidget(self.slider_alpha)

        config_layout.addWidget(QtWidgets.QLabel("Blend"))
        config_layout.addWidget(QtWidgets.QLabel("Source"))
        self.init_combo_box_blend_src()
        config_layout.addWidget(self.combo_box_blend_src)
        config_layout.addWidget(QtWidgets.QLabel("Destination"))
        self.init_combo_box_blend_dest()
        config_layout.addWidget(self.combo_box_blend_dest)

        main_layout.addLayout(config_layout)
        self.setLayout(main_layout)
        self.setMinimumSize(720, 500)

    def init_combo_box_figures(self):
        self.combo_box_figure = QtWidgets.QComboBox(self)
        self.combo_box_figure.addItem("Points")
        self.combo_box_figure.addItem("Lines")
        self.combo_box_figure.addItem("Line Strip")
        self.combo_box_figure.addItem("Line Loop")
        self.combo_box_figure.addItem("Triangles")
        self.combo_box_figure.addItem("Triangle Strip")
        self.combo_box_figure.addItem("Triangle Fan")
        self.combo_box_figure.addItem("Quads")
        self.combo_box_figure.addItem("Quad Strip")
        self.combo_box_figure.addItem("Poligon")
        self.combo_box_figure.currentIndexChanged.connect(self.update_figures)

    def init_scissor_utils(self):
        self.scissor_range_x1 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.scissor_range_x1.setRange(0, MAX_SLIDER_VALUE)
        self.scissor_range_x1.setValue(0)
        self.scissor_range_x1.valueChanged.connect(self.x1_change)
        self.scissor_range_y1 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.scissor_range_y1.setRange(0, MAX_SLIDER_VALUE)
        self.scissor_range_y1.setValue(0)
        self.scissor_range_y1.valueChanged.connect(self.y1_change)
        self.scissor_range_x2 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.scissor_range_x2.setRange(0, MAX_SLIDER_VALUE)
        self.scissor_range_x2.setValue(MAX_SLIDER_VALUE)
        self.scissor_range_x2.valueChanged.connect(self.x2_change)
        self.scissor_range_y2 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.scissor_range_y2.setRange(0, MAX_SLIDER_VALUE)
        self.scissor_range_y2.setValue(MAX_SLIDER_VALUE)
        self.scissor_range_y2.valueChanged.connect(self.y2_change)

    def init_combo_box_alpha(self):
        self.combo_box_alpha = QtWidgets.QComboBox(self)
        self.combo_box_alpha.addItem("GL_ALWAYS")
        self.combo_box_alpha.addItem("GL_NEVER")
        self.combo_box_alpha.addItem("GL_LESS")
        self.combo_box_alpha.addItem("GL_EQUAL")
        self.combo_box_alpha.addItem("GL_LEQUAL")
        self.combo_box_alpha.addItem("GL_GREATER")
        self.combo_box_alpha.addItem("GL_NOTEQUAL")
        self.combo_box_alpha.addItem("GL_GEQUAL")
        self.combo_box_alpha.currentIndexChanged.connect(self.update_alpha)

    def init_combo_box_blend_src(self):
        self.combo_box_blend_src = QtWidgets.QComboBox(self)
        self.combo_box_blend_src.addItem("GL_ONE")
        self.combo_box_blend_src.addItem("GL_ZERO")
        self.combo_box_blend_src.addItem("GL_DST_COLOR")
        self.combo_box_blend_src.addItem("GL_ONE_MINUS_DST_COLOR")
        self.combo_box_blend_src.addItem("GL_SRC_ALPHA")
        self.combo_box_blend_src.addItem("GL_ONE_MINUS_SRC_ALPHA")
        self.combo_box_blend_src.addItem("GL_DST_ALPHA")
        self.combo_box_blend_src.addItem("GL_ONE_MINUS_DST_ALPHA")
        self.combo_box_blend_src.addItem("GL_SRC_ALPHA_SATURATE")
        self.combo_box_blend_src.currentIndexChanged.connect(self.update_blend_src)

    def init_combo_box_blend_dest(self):
        self.combo_box_blend_dest = QtWidgets.QComboBox(self)
        self.combo_box_blend_dest.addItem("GL_ZERO")
        self.combo_box_blend_dest.addItem("GL_ONE")
        self.combo_box_blend_dest.addItem("GL_SRC_COLOR")
        self.combo_box_blend_dest.addItem("GL_ONE_MINUS_SRC_COLOR")
        self.combo_box_blend_dest.addItem("GL_SRC_ALPHA")
        self.combo_box_blend_dest.addItem("GL_ONE_MINUS_SRC_ALPHA")
        self.combo_box_blend_dest.addItem("GL_DST_ALPHA")
        self.combo_box_blend_dest.addItem("GL_ONE_MINUS_DST_ALPHA")
        self.combo_box_blend_dest.currentIndexChanged.connect(self.update_blend_dest)

    @scissor
    def x1_change(self):
        if self.scissor_range_x1.value() > self.scissor_range_x2.value():
            self.scissor_range_x1.setValue(self.scissor_range_x2.value())

    @scissor
    def y1_change(self):
        if self.scissor_range_y1.value() > self.scissor_range_y2.value():
            self.scissor_range_y1.setValue(self.scissor_range_y2.value())

    @scissor
    def x2_change(self):
        if self.scissor_range_x2.value() < self.scissor_range_x1.value():
            self.scissor_range_x2.setValue(self.scissor_range_x1.value())

    @scissor
    def y2_change(self):
        if self.scissor_range_y2.value() < self.scissor_range_y1.value():
            self.scissor_range_y2.setValue(self.scissor_range_y1.value())

    def update_figures(self, index):
        self.widget.update_figure(index=index)

    def update_n_figures(self, text):
        if text:
            if text in ["-", "+"]:
                text = 0
            if int(text) > 100_000:
                text = 100_000
            if int(text) < 0:
                text = 0
        else:
            text = 0
        self.line_edit_n_points.setText(str(text) if text != 0 else "")
        self.widget.update_figure(n=int(text))

    def update_alpha(self, index):
        self.widget.update_alpha(index)

    def update_alpha_value(self):
        self.widget.update_alpha_value(self.slider_alpha.value()/MAX_SLIDER_VALUE)

    def update_blend_src(self, index):
        self.widget.update_blend_src(index)

    def update_blend_dest(self, index):
        self.widget.update_blend_src(index)

    def update_checkbox(self, state):
        self.line_edit_n_points.setDisabled(state)
        self.widget.update_presets_flag(state)
