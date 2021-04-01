cmake_minimum_required(VERSION 3.17)
project(Lb5)
set(CMAKE_CXX_STANDARD 20)

find_package(Qt5Widgets)
find_package(Qt5OpenGL)
set(CMAKE_AUTOMOC ON)

find_package(OpenGL)

set(QT_VERSION 5)
set(PROJECT_HEADERS
        gui/Widgets.h
        gui/MainWindow.h
        )
set(PROJECT_SOURCES
        gui/Widgets.cpp
        gui/MainWindow.cpp
        main.cpp
        )

add_executable(${PROJECT_NAME}  ${PROJECT_SOURCES} ${PROJECT_HEADERS})
qt5_use_modules(${PROJECT_NAME} Widgets OpenGL)
target_link_libraries(${PROJECT_NAME} ${QT_LIBRARIES} ${OPENGL_LIBRARIES})
