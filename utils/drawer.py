import logging

import numpy as np
from OpenGL.GL import *

from utils.matrix import lookat, identity, ortho


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


def get_pts():
    pts = []
    a1 = 1.5e-1
    a2 = 2.e-1
    a3 = 2.5e-1
    omc = 500
    etc = 500
    omega = np.linspace(-np.pi, np.pi, omc)
    eta = np.linspace(-np.pi / 2, np.pi / 2, etc)
    x = a1 * np.cos(eta) * np.cos(omega)
    y = a2 * np.cos(eta) * np.sin(omega)
    z = a3 * np.sin(eta)
    return [y for x in zip(x, y, z) for y in x]


class Drawer:
    def __init__(self, shaders_handler):
        self._pts = [[-0.5, -0.5, 0.], [.5, .5, 0.]]
        self._shaders_program_id = shaders_handler.get_program()
        self._model_matrix_id = glGetUniformLocation(self._shaders_program_id, "modelMat")
        self._view_matrix_id = glGetUniformLocation(self._shaders_program_id, "viewMat")
        self._proj_matrix_id = glGetUniformLocation(self._shaders_program_id, "projMat")
        self._vert_index = glGetAttribLocation(self._shaders_program_id, "aVert")

    def draw(self):
        # s = 0.2
        # quadV = [
        #     -s, s, 0.0,
        #     -s, -s, 0.0,
        #     s, s, 0.0,
        #     s, s, 0.0,
        #     -s, -s, 0.0,
        #     s, -s, 0.0
        # ]
        pts = get_pts()
        np.random.shuffle(pts)
        print(pts)
        # vertices
        vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        vertex_data = np.array(pts, np.float32)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(vertex_data), vertex_data,
                     GL_STATIC_DRAW)
        glUseProgram(self._shaders_program_id)
        proj_matrix = ortho(-2, 2, -2, 2, -20, 20)
        glUniformMatrix4fv(self._proj_matrix_id, 1, GL_FALSE, proj_matrix)
        view_matrix = lookat(np.array([0, 1, 1]), np.array([0, 0, 0]), np.array([0, 1, 0]))
        glUniformMatrix4fv(self._view_matrix_id, 1, GL_FALSE, view_matrix)
        model_matrix = identity(4)
        glUniformMatrix4fv(self._model_matrix_id, 1, GL_FALSE, model_matrix)

        glEnableVertexAttribArray(self._vert_index)

        # set buffers
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        glVertexAttribPointer(self._vert_index, 3, GL_FLOAT, GL_FALSE, 0, None)

        # draw
        glDrawArrays(GL_TRIANGLES, 0, len(pts))

        # disable arrays
        glDisableVertexAttribArray(self._vert_index)
