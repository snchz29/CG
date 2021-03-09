from OpenGL.GL import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtOpenGL import QGLWidget


class DrawArea(QGLWidget):
    def __init__(self, control_panel):
        self._control_panel = control_panel
        super().__init__()
        self.setMinimumSize(600, 480)
        self.resize(600, 480)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self._control_panel.paint()

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(255, 255, 255))
        glLineWidth(1)
        self.qglColor(QtGui.QColor(255, 0, 0))

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def update(self):
        self.updateGL()
