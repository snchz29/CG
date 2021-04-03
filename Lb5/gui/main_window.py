import subprocess
import sys
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QFileDialog, QPushButton, QVBoxLayout

script = "./main.out"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nechepurenko & Terekhov Ltd.")
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        self._welcoming_lbl = QLabel("Лабораторная работа №5"
                                     "\nРасширения OpenGL, программируемый графический конвейер."
                                     "\nШейдеры."
                                     "\nгр.8382 Терехов А.Е, Нечепуренко Н.А.")
        self._choose_file_lbl = QLabel("Выберите путь до изображения")
        self._choose_file_btn = QPushButton("Выбрать...")
        self._choose_file_btn.clicked.connect(self._choose_file_lbl_clicked)
        self._inner_layout = QHBoxLayout()
        self._inner_widget = QWidget()
        self._inner_widget.setLayout(self._inner_layout)
        self._inner_layout.addWidget(self._choose_file_lbl)
        self._inner_layout.addWidget(self._choose_file_btn)
        self._main_layout.addWidget(self._welcoming_lbl)
        self._main_layout.addWidget(self._inner_widget)
        self.setMaximumSize(700, 480)

    def _choose_file_lbl_clicked(self):
        file = QFileDialog().getOpenFileName(self)
        path = file[0]
        if path:
            subprocess.call([script, path])
