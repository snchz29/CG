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

ControlPanel::~ControlPanel() {
    delete this->drawArea;
    delete this->mainLayout;
    delete this->labelHeader;
}

DrawArea::DrawArea(ControlPanel *cPanel, QGLWidget *parent) : QGLWidget(parent),
                                                              controlPanel(cPanel) {
    this->shaderRenderer = new ShaderRenderer();
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

DrawArea::~DrawArea() {
    delete this->controlPanel;
    delete this->shaderRenderer;
}


ShaderRenderer::ShaderRenderer(){

}
