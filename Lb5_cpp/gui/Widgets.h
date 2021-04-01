#ifndef LB5_WIDGETS_H
#define LB5_WIDGETS_H

#include <QWidget>
#include <QVBoxLayout>
#include <QLabel>

#include <QOpenGLWidget>

class DrawArea;

class ControlPanel : public QWidget {
public:
    explicit ControlPanel(QWidget * = nullptr);

    void setDrawArea(DrawArea *);

private:
    DrawArea *drawArea;
    QVBoxLayout *mainLayout;
    QLabel *labelHeader;
};

class DrawArea : public QOpenGLWidget {
public:
    explicit DrawArea(ControlPanel *, QOpenGLWidget * = nullptr);

private:
    ControlPanel *controlPanel;

};


#endif //LB5_WIDGETS_H
