import logging

import PIL.Image as Image
import numpy as np
from OpenGL.GL import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtOpenGL import *


class ShaderRenderer:
    def __init__(self):
        self._shaders_program = None
        self._uniform_image_cover_location = None

    def init(self):
        self._initialize_shaders()
        self._texture = self._initialize_texture()
        self._pass_uniform()

    def _pass_uniform(self):
        self._uniform_image_cover_location = glGetUniformLocation(self._shaders_program,
                                                                  "uniformImageCover")
        glUniform1f(self._uniform_image_cover_location, self._texture)

    def _initialize_texture(self, path="resources/images/test.jpg"):
        image = Image.open(path)
        img_data = np.array(list(image.getdata()), np.int8)
        texture_id = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        return texture_id

    def _initialize_shaders(self):
        vertex_shader, fragment_shader = self._create_vertex_shader(), self._create_fragment_shader()
        self._shaders_program = glCreateProgram()
        glAttachShader(self._shaders_program, vertex_shader)
        glAttachShader(self._shaders_program, fragment_shader)
        glLinkProgram(self._shaders_program)
        glUseProgram(self._shaders_program)
        result = glGetProgramiv(self._shaders_program, GL_LINK_STATUS)
        if not result:
            raise RuntimeError(glGetProgramInfoLog(self._shaders_program))

    def _create_vertex_shader(self):
        vertex_shader_code = self._read_shader_code("shaders/vertex.glsl")
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vertex_shader_code)
        glCompileShader(vertex_shader)
        result = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
        if not result:
            raise RuntimeError(glGetShaderInfoLog(vertex_shader))
        return vertex_shader

    def _create_fragment_shader(self):
        fragment_shader_code = self._read_shader_code("shaders/fragment.glsl")
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_shader_code)
        glCompileShader(fragment_shader)
        result = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
        if not result:
            raise RuntimeError(glGetShaderInfoLog(fragment_shader))
        return fragment_shader

    def _read_shader_code(self, path):
        try:
            with open(path, "r") as f:
                shader_code = f.read()
        except IOError:
            logging.info(f"Unable to load shader code for path {path}")
            raise ArgumentError(f"Cannot load shader code for path {path}")
        return shader_code


class DrawArea(QGLWidget):
    def __init__(self, control_panel):
        self._control_panel = control_panel
        self._shader_renderer = ShaderRenderer()
        super().__init__()
        self.setMinimumSize(600, 480)
        self.resize(600, 480)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_POLYGON)
        glVertex2d(-1.0, -1.0)
        glVertex2d(-1.0, 1.0)
        glVertex2d(1.0, -1.0)
        glVertex2d(1.0, 1.0)
        glEnd()
        #glEnableVertexAttribArray(0)
        # these vertices contain 2 single precision coordinates
        #glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        # draw "count" points from the VBO
        # self._control_panel.paint()

    def initializeGL(self):
        try:
            self._shader_renderer.init()
        except Exception as e:
            logging.info(e)
        self.qglClearColor(QtGui.QColor(255, 255, 255))
        glLineWidth(1)
        # self.qglColor(QtGui.QColor(255, 0, 0))

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def update(self):
        self.updateGL()
