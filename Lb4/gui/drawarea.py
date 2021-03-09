from OpenGL.GL import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtOpenGL import QGLWidget

from Lb4.core.drawer import Drawer


class DrawArea(QGLWidget):
    def __init__(self):
        self._drawer = Drawer()
        super().__init__()
        self.setMinimumSize(600, 480)
        self.resize(600, 480)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self._drawer.paint()

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(255, 255, 255))
        glLineWidth(1)
        self.qglColor(QtGui.QColor(255, 0, 0))

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def get_drawer(self):
        return self._drawer

    def update(self):
        self.updateGL()
