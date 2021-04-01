#include "MainWindow.h"

MainWindow::MainWindow(QWidget *parent) : QWidget(parent) {
    this->setWindowTitle("Nechepurenko & Terekhov Ltd.");
    this->setMinimumSize(700, 480);
    this->mainLayout = new QHBoxLayout();
    this->setLayout(this->mainLayout);
    this->controlPanel = new ControlPanel();
    this->drawArea = new DrawArea(this->controlPanel);
    this->controlPanel->setDrawArea(this->drawArea);
    this->mainLayout->addWidget(this->drawArea);
    this->mainLayout->addWidget(this->controlPanel);

}
