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

DrawArea::DrawArea(ControlPanel *cPanel, QOpenGLWidget *parent) : QOpenGLWidget(parent),
                                                                  controlPanel(cPanel) {
    this->setMinimumSize(600, 480);
    this->resize(600, 480);
    this->setFocusPolicy(Qt::StrongFocus);
}
