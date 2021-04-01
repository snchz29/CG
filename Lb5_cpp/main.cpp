#include <QApplication>
#include "gui/MainWindow.h"

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    auto ui = new MainWindow();
    ui->show();
    return QApplication::exec();
}
