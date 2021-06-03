from PyQt5.QtWidgets import QWidget, QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from gui.drawarea import DrawArea
from gui.panel import ControlPanel
from utils.mediator import Mediator


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nechepurenko & Terekhov Ltd.")
        self._main_layout = QHBoxLayout()
        self.setLayout(self._main_layout)
        mediator = Mediator()
        self._draw_area = DrawArea(mediator)
        self._main_layout.addWidget(self._draw_area)
        self._control_group_scroll = QScrollArea()
        self._control_group_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._main_layout.addWidget(self._control_group_scroll)
        self._control_panel = ControlPanel(self._draw_area)
        self._control_group_scroll.setWidget(self._control_panel)
        self.setMaximumSize(850, 480)
