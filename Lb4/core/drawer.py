import logging
import random
import math

from OpenGL.GL import *


class IFSFractalGenerator:
    def __init__(self, params_list):
        self._function_generator = lambda a, b, c, d, e, f: lambda x0, y0: (a * x0 + b * y0 + e, c * x0 + d * y0 + f)
        self._functions = [self._function_generator(*params) for params in params_list]

    def getNext(self, xx, yy):
        return random.choice(self._functions)(xx, yy)


class Drawer:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._fractal_generator = IFSFractalGenerator(leaf_params)

    def paint(self):
        num_iterations = 100000
        t_X, t_Y = self._x, self._y
        glColor3f(1., 0., 0.)
        glBegin(GL_POINTS)
        for i in range(num_iterations):
            try:
                t_X, t_Y = self._fractal_generator.getNext(t_X, t_Y)
            except Exception as e:
                logging.error(e)
            # logging.info(f"{t_X}, {t_Y}")
            glVertex2f(t_X * 1 / 2, t_Y * 1 / 2)

        glEnd()


leaf_params = [
    [1., 0., 0., 1., -.02, .69],
    [1 / 2, -math.sqrt(3) / 2, math.sqrt(3) / 2, 1 / 2, .8, -.12],
    [0.423, 0.906, -0.906, 0.423, -.75, -.19],
    [1, 0, 0, 1, .01, -.28],
    [.13, 0, 0, .43, .03, -.73]
]

for index in range(len(leaf_params)):
    for inx2 in range(len(leaf_params[index])):
        if inx2 < 4:
            leaf_params[index][inx2] *= 1 / 2
