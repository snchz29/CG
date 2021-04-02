#ifndef LB5_WIDGETS_H
#define LB5_WIDGETS_H

#include <iostream>
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

    ~ControlPanel();

private:
    DrawArea *drawArea;
    QVBoxLayout *mainLayout;
    QLabel *labelHeader;
};

class DrawArea : public QGLWidget {
public:
    explicit DrawArea(ControlPanel *, QGLWidget * = nullptr);

    ~DrawArea();

    void update();
protected:
    void resizeGL(int w, int h) override;

    void initializeGL() override;

    void paintGL() override;

private:
    ControlPanel *controlPanel;

    ShaderRenderer *shaderRenderer;
};


#endif //LB5_WIDGETS_H
