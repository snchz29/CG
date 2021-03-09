import math
import random

from OpenGL.GL import *


class Drawer:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._rec_fractal_generator = RecFractalGenerator()

    def paint(self):
        sqs = self._rec_fractal_generator.get()
        colors = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ]
        idx = 0
        for s in sqs:
            glColor3f(1,0,0)
            idx = (idx + 1) % len(colors)
            glBegin(GL_LINE_LOOP)
            glVertex2f(s[0][0] * 1, s[0][1] * 1)
            glVertex2f(s[1][0] * 1, s[1][1] * 1)
            glVertex2f(s[2][0] * 1, s[2][1] * 1)
            glVertex2f(s[3][0] * 1, s[3][1] * 1)
            glEnd()


class RecFractalGenerator:
    rot = [
        [math.cos, lambda theta: -math.sin(theta)],
        [math.sin, math.cos],
    ]

    def __init__(self):
        self._start_shape = [
            [-1, 1],
            [1, 1],
            [1, -1],
            [-1, -1],
        ]
        self._sqs = []
        self._max_depth = 5
        self._params = [
            [0, 1, 1, 0, -.4],
            [0, 1, 1, 0, .4],
            [- 60, 1, 1, -.5, -.2],
            [60, 1, 1, .5, -.2],
            [0, .1, .5, 0, -2.4],
        ]

    def get(self):
        self.rec(self._start_shape, *self._params[0])
        self.rec(self._start_shape, *self._params[1])
        self.rec(self._start_shape, *self._params[2])
        self.rec(self._start_shape, *self._params[3])
        self.rec(self._start_shape, *self._params[4])
        self._sqs = list(filter(lambda x: x is not None, self._sqs))
        return self._sqs

    def rec(self, shape: list, theta: float = 0, dx: float = 1, dy: float = 1, cx: float = 0, cy: float = 0, depth=0):
        new_shape = []
        if depth > self._max_depth:
            return
        for s in shape:
            new_shape.append(
                [(self.rot[0][0](theta) * s[0] + cx) * dx * .5 + (self.rot[0][1](theta) * s[1] + cx) * dy * .5,
                 (self.rot[1][0](theta) * s[0] + cy) * dx * .5 + (self.rot[1][1](theta) * s[1] + cy) * dy * .5])
        if depth == self._max_depth - 1:
            self._sqs.append(self.rec(new_shape, *self._params[0], depth + 1))
            self._sqs.append(self.rec(new_shape, *self._params[1], depth + 1))
            self._sqs.append(self.rec(new_shape, *self._params[2], depth + 1))
            self._sqs.append(self.rec(new_shape, *self._params[3], depth + 1))
            self._sqs.append(self.rec(new_shape, *self._params[4], depth + 1))
        else:
            self.rec(new_shape, *self._params[0], depth + 1)
            self.rec(new_shape, *self._params[1], depth + 1)
            self.rec(new_shape, *self._params[2], depth + 1)
            self.rec(new_shape, *self._params[3], depth + 1)
            self.rec(new_shape, *self._params[4], depth + 1)
        return new_shape
