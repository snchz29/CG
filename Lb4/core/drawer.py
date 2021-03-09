import math
import random

from OpenGL.GL import *


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class IFSFractalGenerator:
    def __init__(self, params_list):
        self._function_generator = lambda a, b, c, d, e, f: lambda x0, y0: (a * x0 + b * y0 + e, c * x0 + d * y0 + f)
        self._functions = [self._function_generator(*params) for params in params_list]
        self._functions_size = self._functions.__len__()

    def getNext(self, previous_x, previous_y):
        fn_index = random.randint(0, self._functions_size - 1)
        return fn_index, self._functions[fn_index](previous_x, previous_y)


class Drawer(metaclass=SingletonMeta):

    def __init__(self):
        self._x = 0
        self._y = 0
        self._fractal_generator = IFSFractalGenerator(leaf_params)

    def paint(self, num_iterations=100000, color_mode=False):
        current_x, current_y = self._x, self._y
        glBegin(GL_POINTS)
        glColor3f(1., 0., 0.)
        for i in range(num_iterations):
            color_index, (current_x, current_y) = self._fractal_generator.getNext(current_x, current_y)
            if color_mode:
                glColor3f(*color_params[color_index])
            glVertex2f(current_x * 1 / 2, current_y * 1 / 2)

        glEnd()


colors = [
    [1., 0., 0.],
    [0., 1., 0.],
    [0., 0., 1.],
    [1., 0., 1.],
    [1., .5, 0]
]

color_params = {index: color for index, color in enumerate(colors)}

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
