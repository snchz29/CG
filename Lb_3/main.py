import sys
from PyQt5.QtWidgets import QApplication

from gui.MainWindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
