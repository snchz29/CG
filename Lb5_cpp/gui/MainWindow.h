#ifndef LB5_MAINWINDOW_H
#define LB5_MAINWINDOW_H
#include <QWidget>
#include <QHBoxLayout>
#include "Widgets.h"

class MainWindow: public QWidget {
public:
    MainWindow(QWidget *parent = nullptr);

    virtual ~MainWindow();

private:
    QHBoxLayout* mainLayout;
    ControlPanel* controlPanel;
    DrawArea* drawArea{};

};


#endif //LB5_MAINWINDOW_H
