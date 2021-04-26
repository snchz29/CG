import ctypes
import logging

import numpy as np
from OpenGL.GL import *

from utils.ellipsoid import get_pts, get_indices
from utils.matrix import lookat, identity, ortho, rotz, roty


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
        self._camera_pos = np.array([0., 0., 0.])
        self._camera_front = np.array([0., 0., -1.])
        self._camera_up = np.array([0., 1., 0.])
        self._phi = 0
        self._psi = 0

    def draw(self):
        self._draw_axis()
        self._draw_ellipsoid()

    def _draw_ellipsoid(self):
        points_amount_in_a_row = 8
        ellipsoid_points = get_pts(points_amount_in_a_row)

        vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        vertex_data = np.array(ellipsoid_points, np.float32)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(vertex_data), vertex_data,
                     GL_STATIC_DRAW)
        glUseProgram(self._shaders_program_id)
        self._set_matrices()

        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glDrawArrays(GL_TRIANGLES, 0, len(vertex_data))

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glUseProgram(0)

    def _set_matrices(self):
        light_pos = np.array([0., 0., 0.])
        glUniform3fv(self._light_pos_id, 1, GL_FALSE, light_pos)
        proj_matrix = ortho(-2, 2, -2, 2, -20, 20)
        glUniformMatrix4fv(self._proj_matrix_id, 1, GL_FALSE, proj_matrix)
        view_matrix = lookat(self._camera_pos,
                             self._camera_pos - self._camera_front, self._camera_up)
        glUniformMatrix4fv(self._view_matrix_id, 1, GL_FALSE, view_matrix)
        model_matrix = identity(4)
        model_matrix = rotz(self._phi).dot(roty(self._psi))
        glUniformMatrix4fv(self._model_matrix_id, 1, GL_FALSE, model_matrix)

    def _draw_axis(self):
        #glUseProgram(self._shaders_program_id)
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
        logging.info(key)
        camera_speed = 0.1
        if key == 87:
            self._camera_pos += camera_speed * self._camera_front
        if key == 83:
            self._camera_pos -= camera_speed * self._camera_front
        if key == 65:
            self._camera_pos -= 8e-2*np.cross(self._camera_front, self._camera_up)
        if key == 68:
            self._camera_pos += 8e-2*np.cross(self._camera_front, self._camera_up)
        if key == 16777234: #AL
            self._psi += 5
        if key == 16777236: #AR
            self._psi -= 5
        if key == 16777235:
            self._phi -= 5
        if key == 16777237:
            self._phi += 5
