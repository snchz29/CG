#include "Widgets.h"

ControlPanel::ControlPanel(QWidget *parent) : QWidget(parent), drawArea(nullptr) {
    this->mainLayout = new QVBoxLayout();
    this->setLayout(this->mainLayout);
    this->mainLayout->setAlignment(Qt::AlignTop);
    this->labelHeader = new QLabel("Лабораторная работа № 5\nШейдеры\n8382 Нечепуренко Н.А., Терехов А.Е.");
    this->mainLayout->addWidget(this->labelHeader);
}

void ControlPanel::setDrawArea(DrawArea *dArea) {
    this->drawArea = dArea;
}

DrawArea::DrawArea(ControlPanel *cPanel, QGLWidget *parent) : QGLWidget(parent),
                                                              controlPanel(cPanel) {
    this->setMinimumSize(600, 480);
    this->resize(600, 480);
    this->setFocusPolicy(Qt::StrongFocus);
}

void DrawArea::paintGL() {
    glClear(GL_COLOR_BUFFER_BIT);
    glBegin(GL_POLYGON);
    glVertex2d(-1.0, -1.0);
    glVertex2d(-1.0, 1.0);
    glVertex2d(1.0, -1.0);
    glVertex2d(1.0, 1.0);
    glEnd();
}

void DrawArea::initializeGL() {
    this->qglClearColor(QColor(255, 255, 255));
    glLineWidth(1);
}

void DrawArea::resizeGL(int w, int h) {
    glViewport(0, 0, w, h);
}

void DrawArea::update() {
    this->updateGL();
}


ShaderRenderer::ShaderRenderer(){
    const char *vertexShaderSource = "#version 330 core\n"
                                     "layout (location = 0) in vec3 aPos;\n"
                                     "void main()\n"
                                     "{\n"
                                     "   gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n"
                                     "}\0";
    unsigned int vertexShader;
    vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexShaderSource, nullptr);
    glCompileShader(vertexShader);
    int  success;
    char infoLog[512];
    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
}
