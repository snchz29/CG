from PyQt5.QtWidgets import QVBoxLayout, QWidget

from Lb_3.gui.drawarea import DrawArea


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nechepurenko & Terekhov Ltd.")
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        self._draw_area = DrawArea()
        self._main_layout.addWidget(self._draw_area)
        self.setMaximumSize(600, 480)
