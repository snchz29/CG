from PyQt5.QtWidgets import QWidget, QHBoxLayout

from Lb5.gui.control_panel import ControlPanel
from Lb5.gui.drawarea import DrawArea


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nechepurenko & Terekhov Ltd.")
        self._main_layout = QHBoxLayout()
        self.setLayout(self._main_layout)
        self._control_panel = ControlPanel()
        self._draw_area = DrawArea(self._control_panel)
        self._control_panel.set_draw_area(self._draw_area)
        self._main_layout.addWidget(self._draw_area)
        self._main_layout.addWidget(self._control_panel)
        self.setMaximumSize(700, 480)
