import logging
import sys
from PyQt5.QtWidgets import QApplication

from Lb5.gui.main_window import MainWindow


if __name__ == '__main__':
    format_ = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format_, level=logging.INFO, datefmt="%H:%M:%S")
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())