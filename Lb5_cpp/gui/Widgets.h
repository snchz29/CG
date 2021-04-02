#ifndef LB5_WIDGETS_H
#define LB5_WIDGETS_H

#include <GL/glew.h>
#include <GL/gl.h>
#include <QWidget>
#include <QVBoxLayout>
#include <QLabel>
#include <QGLWidget>

class ShaderRenderer{
public:
    ShaderRenderer();

private:

};

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

class DrawArea : public QGLWidget {
public:
    explicit DrawArea(ControlPanel *, QGLWidget * = nullptr);

    void update();
protected:
    void resizeGL(int w, int h) override;

    void initializeGL() override;

    void paintGL() override;

private:
    ControlPanel *controlPanel;

};


#endif //LB5_WIDGETS_H
