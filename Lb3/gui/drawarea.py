from OpenGL.GL import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtOpenGL import QGLWidget

from Lb_3.utils.core import Drawer


class DrawArea(QGLWidget):
    def __init__(self, mediator):
        self._drawer = Drawer(mediator)
        mediator.register_drawarea(self)
        mediator.register_drawer(self._drawer)
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

    def mousePressEvent(self, event):
        self._drawer.handle_click((2 * event.x() - self.width()) / self.width(),
                                  (2 * (self.height() - event.y()) - self.height()) / self.height())
        self.updateGL()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        self._drawer.handle_button(event.key())
        self.updateGL()

    def update(self):
        self.updateGL()
