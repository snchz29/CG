from PyQt5.QtWidgets import QWidget, QHBoxLayout

from Lb_3.gui.drawarea import DrawArea
from Lb_3.gui.panel import ControlPanel
from Lb_3.utils.mediator import Mediator


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
