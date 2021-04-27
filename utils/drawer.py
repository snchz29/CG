import logging

import numpy as np
from OpenGL.GL import *

from utils.ellipsoid import get_pts
from utils.matrix import lookat, identity, ortho, rotz, roty, perspective, frustum


def get_file_content(path):
    try:
        with open(path, "r") as f:
            content = " ".join(f.readlines())
    except IOError:
        logging.info(f"Unable to load content for path {path}")
        raise ArgumentError(f"Cannot load content for path {path}")
    return content


def create_vertex_shader():
    vertex_shader_code = get_file_content("shaders/vertex.vs")
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_code)
    glCompileShader(vertex_shader)
    result = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
    if not result:
        raise RuntimeError(glGetShaderInfoLog(vertex_shader))
    return vertex_shader


def create_fragment_shader():
    fragment_shader_code = get_file_content("shaders/fragment.fs")
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_code)
    glCompileShader(fragment_shader)
    result = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
    if not result:
        raise RuntimeError(glGetShaderInfoLog(fragment_shader))
    return fragment_shader


class ShadersHandler:
    def __init__(self):
        self._shaders_program = None

    def init(self):
        self._initialize_shaders()

    def _initialize_shaders(self):
        vertex_shader, fragment_shader = create_vertex_shader(), create_fragment_shader()
        self._shaders_program = glCreateProgram()
        glAttachShader(self._shaders_program, vertex_shader)
        glAttachShader(self._shaders_program, fragment_shader)
        glLinkProgram(self._shaders_program)
        glUseProgram(self._shaders_program)
        result = glGetProgramiv(self._shaders_program, GL_LINK_STATUS)
        if not result:
            raise RuntimeError(glGetProgramInfoLog(self._shaders_program))

    def get_program(self):
        return self._shaders_program


class Drawer:
    def __init__(self, shaders_handler):
        self._pts = [[-0.5, -0.5, 0.], [.5, .5, 0.]]
        self._shaders_program_id = shaders_handler.get_program()
        self._model_matrix_id = glGetUniformLocation(self._shaders_program_id, "modelMat")
        self._view_matrix_id = glGetUniformLocation(self._shaders_program_id, "viewMat")
        self._proj_matrix_id = glGetUniformLocation(self._shaders_program_id, "projMat")
        self._light_pos_id = glGetUniformLocation(self._shaders_program_id, "lightPos")
        self._ambient_strength_id = glGetUniformLocation(self._shaders_program_id, "ambientStrength")
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
        ellipsoid_points = get_pts(self._points_count, self._clipping_level, self._axis_x, self._axis_y, self._axis_z)

        vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        vertex_data = np.array(ellipsoid_points, np.float32)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(vertex_data), vertex_data,
                     GL_STATIC_DRAW)
        glUseProgram(self._shaders_program_id)
        self._set_uniform()

        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glDrawArrays(GL_TRIANGLES, 0, len(vertex_data))

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glUseProgram(0)

    def _set_uniform(self):
        light_pos = np.array([-5.0, -5.0, -5.0])
        glUniform3f(self._light_pos_id, light_pos[0], light_pos[1], light_pos[2])
        glUniform1f(self._ambient_strength_id, self._ambient_strength)
        if self._projection_state:
            proj_matrix = ortho(-2, 2, -2, 2, -20, 20)
        else:
            proj_matrix = frustum(-2, 2, -2, 2, 4.0, 25.0)
        glUniformMatrix4fv(self._proj_matrix_id, 1, GL_FALSE, proj_matrix)
        view_matrix = lookat(self._camera_pos,
                             self._camera_pos - self._camera_front, self._camera_up)
        glUniformMatrix4fv(self._view_matrix_id, 1, GL_FALSE, view_matrix)
        model_matrix = identity(4)
        model_matrix = rotz(self._phi).dot(roty(self._psi))
        glUniformMatrix4fv(self._model_matrix_id, 1, GL_FALSE, model_matrix)

    def _draw_axis(self):
        # glUseProgram(self._shaders_program_id)
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
        glUseProgram(0)

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
