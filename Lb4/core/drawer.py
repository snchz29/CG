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
            [- 60 * math.pi / 180, 1, 1, -.5, -.2],
            [60 * math.pi / 180, 1, 1, .5, -.2],
            [0, .1, .5, 0, -2.4],
        ]

    def get(self, depth):
        self._max_depth = depth
        self._sqs = []
        self.rec(self._start_shape, *self._params[0])
        self.rec(self._start_shape, *self._params[1])
        self.rec(self._start_shape, *self._params[2])
        self.rec(self._start_shape, *self._params[3])
        self.rec(self._start_shape, *self._params[4])
        return list(filter(lambda x: x is not None, self._sqs))

    def rec(self, shape: list, theta: float = 0, dx: float = 1, dy: float = 1, cx: float = 0, cy: float = 0,
            depth=0):
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


class Drawer(metaclass=SingletonMeta):
    def __init__(self):
        self._x = 0
        self._y = 0
        self._fractal_generator = IFSFractalGenerator(leaf_params)
        self._rec_fractal_generator = RecFractalGenerator()

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

    def paint_recursive(self, depth):
        sqs = self._rec_fractal_generator.get(depth)
        for s in sqs:
            glColor3f(1, 0, 0)
            glBegin(GL_LINE_LOOP)
            glVertex2f(s[0][0] * .8, s[0][1] * .8)
            glVertex2f(s[1][0] * .8, s[1][1] * .8)
            glVertex2f(s[2][0] * .8, s[2][1] * .8)
            glVertex2f(s[3][0] * .8, s[3][1] * .8)
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
