import logging
import math
from enum import auto, Enum
from typing import Dict, List

from OpenGL.GL import *

from utils.spline import NURBSpline3deg6points


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Point:
    def __init__(self, x: float = 0., y: float = 0.):
        self._x = x
        self._y = y
        self._segments = 10
        self._radius = 1.2e-2
        self._color = [1., 0., 0.]
        self._weight = 1

    def get_coordinates(self) -> Dict[str, float]:
        return {"x": self._x, "y": self._y}

    def move(self, direction):
        logging.info(f"Move key pressed with direction {direction}")
        if direction == Direction.DOWN:
            self._y = max(-1., self._y - 0.02)
        if direction == Direction.UP:
            self._y = min(1., self._y + 0.02)
        if direction == Direction.LEFT:
            self._x = max(-1., self._x - 0.02)
        if direction == Direction.RIGHT:
            self._x = min(1., self._x + 0.02)

    def get_weight(self) -> int:
        return self._weight

    def set_weight(self, weight: int):
        self._weight = weight

    def set_color(self, color: List[float]):
        self._color = color

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
    def __init__(self, mediator):
        self._points = [
            Point(-.8, -.25),
            Point(-.6, .3),
            Point(-.25, -.6),
            Point(.12, .3),
            Point(.5, -.5),
            Point(.8, .25)
        ]
        self._current_point = None
        self._current_point_idx = None
        self._nurbs = NURBSpline3deg6points(self._points)
        self._mediator = mediator

    def paint(self):
        self._nurbs.set_points(self._points)
        points = self._nurbs.get_nurbs_curve_points()
        glColor3f(0, 0, 1)
        glBegin(GL_LINE_STRIP)
        for point in points:
            glVertex2f(point[0], point[1])
        glEnd()
        for point in self._points:
            point.draw()

    def handle_click(self, x, y):
        candidate_point = Point(x, y)
        for idx, point in enumerate(self._points):
            if point == candidate_point:
                self._set_current_point(idx)
                return

    def _set_current_point(self, idx):
        self._current_point = self._points[idx]
        self._current_point_idx = idx
        for point in self._points:
            point.set_color([1., 0., 0.])
        self._current_point.set_color([0., 1., 1.])
        self._mediator.set_point_info_widget_current_point(self._current_point, self._current_point_idx)
        self._mediator.update()

    def handle_button(self, key_code):
        if self._current_point_idx is not None and key_code == 16777217:
            self._set_current_point((self._current_point_idx + 1) % len(self._points))
        if self._current_point and key_code in key_mapper:
            self._current_point.move(key_mapper.get(key_code))

    def set_new_current_point_weight(self, new_value):
        if self._current_point:
            self._current_point.set_weight(new_value)


key_mapper = {
    87: Direction.UP,
    83: Direction.DOWN,
    65: Direction.LEFT,
    68: Direction.RIGHT,
    16777236: Direction.RIGHT,
    16777234: Direction.LEFT,
    16777235: Direction.UP,
    16777237: Direction.DOWN
}
