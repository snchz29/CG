from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class ControlPanel(QWidget):
    def __init__(self, mediator):
        super().__init__()
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        self._header_label = QLabel("Лабораторная работа № 6\nКаркасные объекты\n8382 Нечепуренко Н.А., Терехов А.Е.")
        self._main_layout.addWidget(self._header_label)
