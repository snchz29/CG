import logging
import random

import numpy as np
from OpenGL.GL import *
from OpenGL.raw.GLU import gluPerspective

from utils.ellipsoid import get_pts
from utils.matrix import lookat, identity, ortho, rotz, roty


class Drawer:
    def __init__(self):
        self._pts = [[-0.5, -0.5, 0.], [.5, .5, 0.]]
        self._ambient_strength = 0.15
        self._camera_pos = np.array([0., 0., 0.])
        self._camera_front = np.array([0., 0., -1.])
        self._camera_up = np.array([0., 1., 0.])
        self._phi = 0
        self._psi = 0
        self._points_count = 8
        self._clipping_level = 0.7
        self._axis_x = 0.9
        self._axis_y = 0.9
        self._axis_z = 0.9
        self._projection_state = 0

    def set_projection_state(self, value):
        self._projection_state = value

    def set_x_axis(self, value):
        self._axis_x = value

    def set_y_axis(self, value):
        self._axis_y = value

    def set_z_axis(self, value):
        self._axis_z = value

    def set_point_count(self, value):
        self._points_count = value

    def set_clipping_level(self, value):
        self._clipping_level = value

    def draw(self):
        self._draw_axis()
        self._draw_ellipsoid()

    def set_ambient(self, value):
        self._ambient_strength = value

    def _draw_ellipsoid(self):
        self._set_uniform()
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        ellipsoid_points = get_pts(self._points_count, self._clipping_level, self._axis_x, self._axis_y, self._axis_z)
        glBegin(GL_TRIANGLES)
        for i in range(0, len(ellipsoid_points), 6):
            glColor4f(1, 0, 1, 1.0)
            glNormal3f(ellipsoid_points[i + 3],
                       ellipsoid_points[i + 4],
                       ellipsoid_points[i + 5])
            glVertex3f(ellipsoid_points[i],
                       ellipsoid_points[i + 1],
                       ellipsoid_points[i + 2])
        glEnd()

    def _set_uniform(self):
        light_pos = np.array([-5.0, -5.0, -5.0, 1.0])
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        if self._projection_state:
            gluPerspective(75, 0, -1, 1)
        else:
            glOrtho(-1, 1, -1, 1, -1, 1)

    def _draw_axis(self):
        glBegin(GL_LINES)

        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(2.0, 0.0, 0.0)

        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 2.0, 0.0)

        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 2.0)
        glEnd()

    def handle_key(self, key):
        camera_speed = 0.1
        if key == 87:
            self._camera_pos -= camera_speed * self._camera_front
            logging.info(f"Moving camera towards")
        if key == 83:
            self._camera_pos += camera_speed * self._camera_front
            logging.info(f"Moving camera backwards")
        if key == 65:
            self._camera_pos -= 8e-2 * np.cross(self._camera_front, self._camera_up)
            logging.info(f"Moving camera to left")
        if key == 68:
            self._camera_pos += 8e-2 * np.cross(self._camera_front, self._camera_up)
            logging.info(f"Moving camera to right")
        if key == 16777234:  # AL
            self._psi -= 5
            logging.info(f"Rotating by psi angle")
        if key == 16777236:  # AR
            self._psi += 5
            logging.info(f"Rotating by psi angle")
        if key == 16777235:
            self._phi += 5
            logging.info(f"Rotating by phi angle")
        if key == 16777237:
            self._phi -= 5
            logging.info(f"Rotating by phi angle")
