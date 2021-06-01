from OpenGL.GL import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtOpenGL import QGLWidget

from utils.drawer import Drawer


class DrawArea(QGLWidget):
    def __init__(self, mediator):
        self._drawer = None
        mediator.register_drawarea(self)
        super().__init__()
        self.setMinimumSize(600, 480)
        self.resize(600, 480)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def paintGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.2980, 0.5843, 0.7098, 1.)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self._drawer.draw()

    def initializeGL(self):
        self._drawer = Drawer()
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

    def set_point_count(self, value):
        self._drawer.set_point_count(value)
        self.paintGL()
        self.update()

    def set_ambient_type(self, value):
        self._drawer.set_ambient_type(value)
        self.paintGL()
        self.update()

    def set_ambient(self, value):
        self._drawer.set_ambient(value)
        self.paintGL()
        self.update()

    def set_shininess_state(self, value):
        self._drawer.set_shininess_state(value)
        self.paintGL()
        self.update()

    def set_clipping_level(self, value):
        self._drawer.set_clipping_level(value)
        self.paintGL()
        self.update()

    def set_x_axis(self, value):
        self._drawer.set_x_axis(value)
        self.paintGL()
        self.update()

    def set_y_axis(self, value):
        self._drawer.set_y_axis(value)
        self.paintGL()
        self.update()

    def set_z_axis(self, value):
        self._drawer.set_z_axis(value)
        self.paintGL()
        self.update()

    def set_projection_state(self, value):
        self._drawer.set_projection_state(value)
        self.paintGL()
        self.update()