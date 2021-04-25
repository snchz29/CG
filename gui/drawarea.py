from OpenGL.GL import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtOpenGL import QGLWidget

from utils.drawer import Drawer, ShadersHandler


class DrawArea(QGLWidget):
    def __init__(self, mediator):
        self._shaders_handler = ShadersHandler()
        self._drawer = None
        mediator.register_drawarea(self)
        super().__init__()
        self.setMinimumSize(600, 480)
        self.resize(600, 480)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def paintGL(self):
        glClearColor(0.2980, 0.5843, 0.7098, 1.)
        glClear(GL_COLOR_BUFFER_BIT)
        self._drawer.draw()

    def initializeGL(self):
        self._shaders_handler.init()
        self._drawer = Drawer(self._shaders_handler)
        self.qglClearColor(QtGui.QColor(255, 255, 255))
        glLineWidth(1)
        self.qglColor(QtGui.QColor(255, 0, 0))

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def get_drawer(self):
        return self._drawer

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        self._drawer.handle_key(event.key())
        self.paintGL()
        self.updateGL()

    def update(self):
        self.updateGL()
