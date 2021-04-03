#include <iostream>
#include <iomanip>

float **generateVertices(int size) {
    float delta = 2.0 / (size - 2);
    float x_pos = 0.5;
    float y_pos = -0.5;
    float x_tex = 1.0;
    float y_tex = 1.0;
    float **arr = new float *[size];
    for (int i = 0; i < size; ++i) {
        arr[i] = new float[8];
        arr[i][0] = x_pos;
        arr[i][1] = y_pos;
        arr[i][2] = 0;
        arr[i][3] = 1;
        arr[i][4] = 1;
        arr[i][5] = 1;
        arr[i][6] = x_tex;
        arr[i][7] = y_tex;
        x_pos -= delta * (i % 2);
        y_pos = -y_pos;
        x_tex -= delta * (i % 2);
        y_tex = std::abs(y_tex - 1);
    }
    return arr;
}

void destroyVertices(float **arr, int size) {
    for (int i = 0; i < size; ++i) {
        delete[] arr[i];
    }
    delete[] arr;
}

int *generateIndices(int n_tr) {
    int *arr = new int[n_tr * 3];
    for (int i = 0; i < n_tr; ++i) {
        for (int j = 0; j < 3; ++j) {
            arr[i * 3 + j] = j + i;
        }
    }
    return arr;
}

void destroyIndices(int *arr) {
    delete[] arr;
}

int main() {
    int tr = 100;
    int ver = tr+2;
    float** vertices = generateVertices(ver);
    int* indices = generateIndices(tr);
    std::cout <<"int n_triangles ="<< tr <<";\n"<<"int n_vertices = n_triangles + 2;"<<std::endl;
    std::cout<< "float vertices[] = {";
    for (int i = 0; i < ver; ++i) {
        for (int j = 0; j < 8; ++j) {
            std::cout << std::fixed << vertices[i][j]<< "f,\t";
        }
        std::cout<<std::endl;
    }
    std::cout<< "};" <<std::endl;
    std::cout<< "unsigned int indices[] = {";

    for (int i = 0; i < tr*3; ++i) {
        std::cout << indices[i]<< ",\t";
    }
    std::cout<< "};" <<std::endl;

    std::cout <<std::endl;

    destroyIndices(indices);
    destroyVertices(vertices, ver);
    return 0;
}