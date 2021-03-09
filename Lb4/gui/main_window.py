from PyQt5.QtWidgets import QWidget, QHBoxLayout

from Lb4.gui.drawarea import DrawArea


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nechepurenko & Terekhov Ltd.")
        self._main_layout = QHBoxLayout()
        self.setLayout(self._main_layout)
        self._draw_area = DrawArea()
        self._main_layout.addWidget(self._draw_area)
        self.setMaximumSize(700, 480)
