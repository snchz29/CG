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


class Drawer(metaclass=SingletonMeta):
    def __init__(self):
        pass

    def paint(self, num_iterations=100000, color_mode=False):
        pass
