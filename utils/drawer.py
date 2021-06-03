import logging
import numpy as np
from OpenGL.GL import *
from OpenGL.raw.GLU import gluPerspective
from utils.ellipsoid import get_pts


class Drawer:
    def __init__(self):
        self._ambient_color = np.array([0, 0, 0, 1])
        self._diffuse_color = np.array([1, 1, 1, 1])
        self._specular_color = np.array([0, 0, 0, 1])
        self._shininess = 0
        self._camera_pos = np.array([0., 0., -2.])
        self._camera_front = np.array([0., 0., -1.])
        self._camera_up = np.array([0., 1., 0.])
        self._phi = 0
        self._psi = 0
        self._points_count = 8
        self._clipping_level = 0.7
        self._axis_x = 0.9
        self._axis_y = 0.9
        self._axis_z = 0.9
        self._projection_state = 2
        self.ortho_x = 2
        self.ortho_y = 2
        self.ortho_z = 2
        self.fov = 90.0

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

    def set_shininess_state(self, value):
        self._shininess = value

    def set_clipping_level(self, value):
        self._clipping_level = value

    def set_ambient_color(self, red, green, blue):
        self._ambient_color = np.array([red, green, blue, 0.1]) / 255

    def set_diffuse_color(self, red, green, blue):
        self._diffuse_color = np.array([red, green, blue, 0.1]) / 255

    def set_specular_color(self, red, green, blue):
        self._specular_color = np.array([red, green, blue, 0.1]) / 255

    def draw(self):
        self._draw_axis()
        self._draw_ellipsoid()

    def _draw_ellipsoid(self):
        glFrontFace(GL_CW)
        self._set_uniform()
        self._set_material()
        self._set_light()
        ellipsoid_points = get_pts(self._points_count, self._clipping_level, self._axis_x, self._axis_y, self._axis_z)
        glBegin(GL_TRIANGLES)
        for i in range(0, len(ellipsoid_points), 6):
            glNormal3f(ellipsoid_points[i + 3],
                       ellipsoid_points[i + 4],
                       ellipsoid_points[i + 5])
            glVertex3f(ellipsoid_points[i],
                       ellipsoid_points[i + 1],
                       ellipsoid_points[i + 2])
        glEnd()

    def _set_light(self):
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, np.array([3.0, 3.0, 3.0, 1.0]))
        glLightfv(GL_LIGHT0, GL_AMBIENT, self._ambient_color)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self._diffuse_color)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self._specular_color)

    def _set_material(self):
        if self._shininess == 2:
            glMaterialfv(GL_FRONT, GL_SPECULAR, self._specular_color)
            glMaterialf(GL_FRONT, GL_SHININESS, 128.0)
        elif self._shininess == 0:
            glMaterialfv(GL_FRONT, GL_SPECULAR, np.array([0, 0, 0, 1]))
            glMaterialf(GL_FRONT, GL_SHININESS, 128.0)

    def _set_uniform(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(self._camera_pos[0], self._camera_pos[1], self._camera_pos[2])
        glRotated(self._phi, 1, 0, 0)
        glRotated(self._psi, 0, 1, 0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self._projection_state == 0:
            gluPerspective(self.fov, 480 / 700, 0.1, 10.0)
        elif self._projection_state == 2:
            glOrtho(-self.ortho_x, self.ortho_x, -self.ortho_y, self.ortho_y, -self.ortho_z, 18+self.ortho_z)

    @staticmethod
    def _draw_axis():
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
            logging.info(f"Moving camera backwards {self._camera_pos}")
        if key == 68:
            self._camera_pos -= 8e-2 * np.cross(self._camera_front, self._camera_up)
            logging.info(f"Moving camera to left")
        if key == 65:
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
