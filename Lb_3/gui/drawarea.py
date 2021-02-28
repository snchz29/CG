import logging
import math
from typing import Dict

from OpenGL.GL import *
from PyQt5 import QtGui
from PyQt5.QtOpenGL import QGLWidget


class DrawArea(QGLWidget):
    def __init__(self):
        self._drawer = Drawer()
        super().__init__()
        self.setMinimumSize(600, 480)
        self.resize(600, 480)

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
        self.updateGL()


class Point:
    def __init__(self, x: float = 0., y: float = 0.):
        self._x = x
        self._y = y
        self._segments = 10
        self._radius = 1.2e-2
        self._color = [1., 0., 0.]

    def get_coordinates(self) -> Dict[str, float]:
        return {"x": self._x, "y": self._y}

    def draw(self):
        glColor3f(*self._color)
        glBegin(GL_TRIANGLE_FAN)
        for segment_index in range(self._segments):
            current_angle = 2. * math.pi * segment_index / self._segments
            x_component = self._radius * math.cos(current_angle)
            y_component = self._radius * math.sin(current_angle)
            glVertex2f(self._x + x_component, self._y + y_component)
        glEnd()

    def get_radius(self):
        return self._radius

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Point):
            return False
        return math.dist((self._x, self._y), other.get_coordinates().values()) <= self._radius

    def __str__(self):
        return f"[Point ({self._x};{self._y}) r={self._radius}, color={self._color}]"


class Drawer:
    def __init__(self):
        self._points = []
        self._points.append(Point(0, 0))
        self._points.append(Point(.9, .9))
        self._points.append(Point(-.5, -.5))

    def paint(self):
        for point in self._points:
            point.draw()
