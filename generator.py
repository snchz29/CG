from random import random


def create_triangle_strip_and_fan(n):
    ret = []
    if n > 0:
        ret.append([(random() - .5) * 2 for i in range(6)])
    if n > 1:
        ret.extend([[(random() - .5) * 2 for i in range(2)] for _ in range(n - 1)])
    return ret


def create_quad_strip(n):
    ret = []
    if n > 0:
        ret.append([(random() - .5) * 2 for i in range(8)])
    if n > 1:
        ret.extend([[(random() - .5) * 2 for i in range(4)] for _ in range(n - 1)])
    return ret


FIGURE_GENERATOR = [
    lambda n: [[(random() - .5) * 2 for i in range(2)] for _ in range(n)],  # n x 2
    lambda n: [[(random() - .5) * 2 for i in range(4)] for _ in range(n)],  # n x 4
    lambda n: [[(random() - .5) * 2 for i in range(2)] for _ in range(n+1)],  # n x 2
    lambda n: [[(random() - .5) * 2 for i in range(2)] for _ in range(n)],  # n x 2
    lambda n: [[(random() - .5) * 2 for i in range(6)] for _ in range(n)],  # n x 6
    create_triangle_strip_and_fan,  # n x 6 + n x 2
    create_triangle_strip_and_fan,  # n x 6 + n x 2
    lambda n: [[(random() - .5) * 2 for i in range(8)] for _ in range(n)],  # n x 8
    create_quad_strip,
    lambda n: [[(random() - .5) * 2 for i in range(2)] for _ in range(n)],  # n x 2
]