from OpenGL.GL import *
from generator import FIGURE_GENERATOR
from PyQt5.QtOpenGL import QGLWidget

FIGURES = [
    GL_POINTS,
    GL_LINES,
    GL_LINE_STRIP,
    GL_LINE_LOOP,
    GL_TRIANGLES,
    GL_TRIANGLE_STRIP,
    GL_TRIANGLE_FAN,
    GL_QUADS,
    GL_QUAD_STRIP,
    GL_POLYGON,
]
ALPHA = [
    GL_ALWAYS,
    GL_NEVER,
    GL_LESS,
    GL_EQUAL,
    GL_LEQUAL,
    GL_GREATER,
    GL_NOTEQUAL,
    GL_GEQUAL,
]
COLORS = [
    (1, 1, 1, 0),       # white
    (1, 0, 0, 7/7),     # red
    (1, .5, 0, 6/7),    # orange
    (1, 1, 0, 5/7),     # yellow
    (0, 1, 0, 4/7),     # green
    (0, 1, 1, 3/7),     # cian
    (0, 0, 1, 2/7),     # blue
    (1, 0, 1, 1/7),     # indigo
]
BLEND_SRC = [
    GL_ONE,
    GL_ZERO,
    GL_DST_COLOR,
    GL_ONE_MINUS_DST_COLOR,
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_DST_ALPHA,
    GL_ONE_MINUS_DST_ALPHA,
    GL_SRC_ALPHA_SATURATE,
]
BLEND_DEST = [
    GL_ZERO,
    GL_ONE,
    GL_SRC_COLOR,
    GL_ONE_MINUS_SRC_COLOR,
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_DST_ALPHA,
    GL_ONE_MINUS_DST_ALPHA,
]
TEST_TRIANGLE_FAN = [
    [0, -1, -1, -1, -.5, -.5],
    [0, 1],
    [.5, -.5],
    [1, -1],
]
TEST_QUAD_STRIP = [
    [-.75, -.25, -.75, .25, -.25, -.75, -.25, .75],
    [.25, -.75, .25, .75],
    [.75, -.25, .75, .25]
]
SIZE_WIDGET = 480


class GLWidget(QGLWidget):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setMinimumSize(SIZE_WIDGET, SIZE_WIDGET)
        self.setMaximumSize(SIZE_WIDGET, SIZE_WIDGET)
        self.n_figures = 50
        self.cur_index_figure = 0
        self.points = FIGURE_GENERATOR[0](self.n_figures)
        self.cur_figure = FIGURES[self.cur_index_figure]
        self.cur_color_index = 0
        self.x_clip = 0
        self.y_clip = 0
        self.w_clip = self.width()
        self.h_clip = self.height()
        self.cur_alpha = 0
        self.alpha_value = 1
        self.blend_src = 0
        self.blend_dest = 1

    def paintGL(self):
        glClearColor(0, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_SCISSOR_TEST)
        glEnable(GL_ALPHA_TEST)
        glEnable(GL_BLEND)
        glAlphaFunc(ALPHA[self.cur_alpha], self.alpha_value)
        glBlendFunc(BLEND_SRC[self.blend_src], BLEND_DEST[self.blend_dest])
        glScissor(self.x_clip, self.y_clip, self.w_clip, self.h_clip)
        self.show_figure()
        glDisable(GL_BLEND)
        glDisable(GL_ALPHA_TEST)
        glDisable(GL_SCISSOR_TEST)

    def resizeGL(self, w: int, h: int):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1.0, 1.0)
        glViewport(0, 0, w, h)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def show_figure(self):
        self.cur_color_index = 0
        glBegin(self.cur_figure)
        for point in self.points:
            color = self.get_color()
            glColor4f(*color)
            glVertex2d(point[0], point[1])
            if len(point) >= 4:
                color = self.get_color()
                glColor4f(*color)
                glVertex2d(point[2], point[3])
            if len(point) >= 6:
                color = self.get_color()
                glColor4f(*color)
                glVertex2d(point[4], point[5])
            if len(point) >= 8:
                color = self.get_color()
                glColor4f(*color)
                glVertex2d(point[6], point[7])
        glEnd()
        glFlush()

    def get_color(self):
        self.cur_color_index = (self.cur_color_index + 1) % len(COLORS)
        return COLORS[self.cur_color_index]

    def update_figure(self, index=None, n=None):
        if index is not None:
            self.cur_index_figure = index
            self.cur_figure = FIGURES[index]
        if n is not None:
            self.n_figures = n
        self.points = FIGURE_GENERATOR[self.cur_index_figure](self.n_figures)
        if self.cur_figure is GL_TRIANGLE_FAN:
            self.points = TEST_TRIANGLE_FAN
        if self.cur_figure is GL_QUAD_STRIP:
            self.points = TEST_QUAD_STRIP
        self.updateGL()

    def scissor(self, x1, y1, x2, y2):
        self.x_clip = int(x1 * self.width())
        self.y_clip = int(y1 * self.height())
        self.w_clip = int((x2 - x1) * self.width())
        self.h_clip = int((y2 - y1) * self.height())
        self.updateGL()

    def update_alpha(self, index):
        self.cur_alpha = index
        self.updateGL()

    def update_alpha_value(self, val):
        self.alpha_value = val
        self.updateGL()

    def update_blend_src(self, index):
        self.blend_src = index
        self.updateGL()

    def update_blend_dest(self, index):
        self.blend_dest = index
        self.updateGL()
