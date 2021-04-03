// g++ glad.c -c
// g++ main.cpp glad.o -lGLEW -lglfw3 -lpthread -lXrandr -lXrender -lXi -lXfixes -lXxf86vm -lXext -lGLEW -lGLU -lm -lGL -lglfw3 -lrt -ldl -lX11 -lxcb -lXau -lXdmcp -o main.out && ./main.out
#define STB_IMAGE_IMPLEMENTATION

#include "glad/glad.h"
#include <GLFW/glfw3.h>

#include "shader_s.h"
#include "stb_image.h"

#include <iostream>

void framebuffer_size_callback(GLFWwindow *window, int width, int height);

void processInput(GLFWwindow *window);

// Константы
const unsigned int SCR_WIDTH = 800;
const unsigned int SCR_HEIGHT = 600;

int main() {
    // glfw: инициализация и конфигурирование    
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

#ifdef __APPLE__
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // раскомментируйте эту строку, если используете macOS
#endif

    // glfw: создание окна
    GLFWwindow *window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "OpenGL for Ravesli.com", NULL, NULL);
    if (window == NULL) {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    // glad: загрузка всех указателей на OpenGL-функции
    if (!gladLoadGLLoader((GLADloadproc) glfwGetProcAddress)) {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    // Компилирование нашей шейдерной программы
    Shader ourShader("texture.vs", "texture.fs");

    // Указание вершин (и буфера(ов)) и настройка вершинных атрибутов
    int n_triangles = 100;
    int n_vertices = n_triangles + 2;

    float vertices[] = {0.500000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	1.000000f,	1.000000f,
                        0.500000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	1.000000f,	0.000000f,
                        0.480000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.980000f,	1.000000f,
                        0.480000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.980000f,	0.000000f,
                        0.460000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.960000f,	1.000000f,
                        0.460000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.960000f,	0.000000f,
                        0.440000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.940000f,	1.000000f,
                        0.440000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.940000f,	0.000000f,
                        0.420000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.920000f,	1.000000f,
                        0.420000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.920000f,	0.000000f,
                        0.400000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.900000f,	1.000000f,
                        0.400000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.900000f,	0.000000f,
                        0.380000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.880000f,	1.000000f,
                        0.380000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.880000f,	0.000000f,
                        0.360000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.860000f,	1.000000f,
                        0.360000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.860000f,	0.000000f,
                        0.340000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.840000f,	1.000000f,
                        0.340000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.840000f,	0.000000f,
                        0.320000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.820000f,	1.000000f,
                        0.320000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.820000f,	0.000000f,
                        0.300000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.800000f,	1.000000f,
                        0.300000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.800000f,	0.000000f,
                        0.280000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.780000f,	1.000000f,
                        0.280000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.780000f,	0.000000f,
                        0.260000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.760000f,	1.000000f,
                        0.260000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.760000f,	0.000000f,
                        0.240000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.740000f,	1.000000f,
                        0.240000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.740000f,	0.000000f,
                        0.220000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.720000f,	1.000000f,
                        0.220000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.720000f,	0.000000f,
                        0.200000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.700000f,	1.000000f,
                        0.200000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.700000f,	0.000000f,
                        0.180000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.680000f,	1.000000f,
                        0.180000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.680000f,	0.000000f,
                        0.160000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.660000f,	1.000000f,
                        0.160000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.660000f,	0.000000f,
                        0.140000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.640000f,	1.000000f,
                        0.140000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.640000f,	0.000000f,
                        0.120000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.620000f,	1.000000f,
                        0.120000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.620000f,	0.000000f,
                        0.100000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.600000f,	1.000000f,
                        0.100000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.600000f,	0.000000f,
                        0.080000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.580000f,	1.000000f,
                        0.080000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.580000f,	0.000000f,
                        0.060000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.560000f,	1.000000f,
                        0.060000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.560000f,	0.000000f,
                        0.040000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.540000f,	1.000000f,
                        0.040000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.540000f,	0.000000f,
                        0.020000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.520000f,	1.000000f,
                        0.020000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.520000f,	0.000000f,
                        -0.000000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.500000f,	1.000000f,
                        -0.000000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.500000f,	0.000000f,
                        -0.020000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.480000f,	1.000000f,
                        -0.020000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.480000f,	0.000000f,
                        -0.040000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.460000f,	1.000000f,
                        -0.040000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.460000f,	0.000000f,
                        -0.060000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.440000f,	1.000000f,
                        -0.060000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.440000f,	0.000000f,
                        -0.080000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.420000f,	1.000000f,
                        -0.080000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.420000f,	0.000000f,
                        -0.100000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.400000f,	1.000000f,
                        -0.100000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.400000f,	0.000000f,
                        -0.120000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.380000f,	1.000000f,
                        -0.120000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.380000f,	0.000000f,
                        -0.140000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.360000f,	1.000000f,
                        -0.140000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.360000f,	0.000000f,
                        -0.160000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.340000f,	1.000000f,
                        -0.160000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.340000f,	0.000000f,
                        -0.180000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.320000f,	1.000000f,
                        -0.180000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.320000f,	0.000000f,
                        -0.200000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.300000f,	1.000000f,
                        -0.200000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.300000f,	0.000000f,
                        -0.220000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.280000f,	1.000000f,
                        -0.220000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.280000f,	0.000000f,
                        -0.240000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.260000f,	1.000000f,
                        -0.240000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.260000f,	0.000000f,
                        -0.260000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.240000f,	1.000000f,
                        -0.260000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.240000f,	0.000000f,
                        -0.280000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.220000f,	1.000000f,
                        -0.280000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.220000f,	0.000000f,
                        -0.300000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.200000f,	1.000000f,
                        -0.300000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.200000f,	0.000000f,
                        -0.320000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.180000f,	1.000000f,
                        -0.320000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.180000f,	0.000000f,
                        -0.340000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.160000f,	1.000000f,
                        -0.340000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.160000f,	0.000000f,
                        -0.360000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.140000f,	1.000000f,
                        -0.360000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.140000f,	0.000000f,
                        -0.380000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.120000f,	1.000000f,
                        -0.380000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.120000f,	0.000000f,
                        -0.400000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.100000f,	1.000000f,
                        -0.400000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.100000f,	0.000000f,
                        -0.420000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.080000f,	1.000000f,
                        -0.420000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.080000f,	0.000000f,
                        -0.440000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.060000f,	1.000000f,
                        -0.440000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.060000f,	0.000000f,
                        -0.460000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.040000f,	1.000000f,
                        -0.460000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.040000f,	0.000000f,
                        -0.480000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.020000f,	1.000000f,
                        -0.480000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.020000f,	0.000000f,
                        -0.500000f,	-0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.000000f,	1.000000f,
                        -0.500000f,	0.500000f,	0.000000f,	1.000000f,	1.000000f,	1.000000f,	0.000000f,	0.000000f,
    };
    unsigned int indices[] = {0,	1,	2,	1,	2,	3,	2,	3,	4,	3,	4,	5,	4,	5,	6,	5,	6,	7,	6,	7,	8,	7,	8,	9,	8,	9,	10,	9,	10,	11,	10,	11,	12,	11,	12,	13,	12,	13,	14,	13,	14,	15,	14,	15,	16,	15,	16,	17,	16,	17,	18,	17,	18,	19,	18,	19,	20,	19,	20,	21,	20,	21,	22,	21,	22,	23,	22,	23,	24,	23,	24,	25,	24,	25,	26,	25,	26,	27,	26,	27,	28,	27,	28,	29,	28,	29,	30,	29,	30,	31,	30,	31,	32,	31,	32,	33,	32,	33,	34,	33,	34,	35,	34,	35,	36,	35,	36,	37,	36,	37,	38,	37,	38,	39,	38,	39,	40,	39,	40,	41,	40,	41,	42,	41,	42,	43,	42,	43,	44,	43,	44,	45,	44,	45,	46,	45,	46,	47,	46,	47,	48,	47,	48,	49,	48,	49,	50,	49,	50,	51,	50,	51,	52,	51,	52,	53,	52,	53,	54,	53,	54,	55,	54,	55,	56,	55,	56,	57,	56,	57,	58,	57,	58,	59,	58,	59,	60,	59,	60,	61,	60,	61,	62,	61,	62,	63,	62,	63,	64,	63,	64,	65,	64,	65,	66,	65,	66,	67,	66,	67,	68,	67,	68,	69,	68,	69,	70,	69,	70,	71,	70,	71,	72,	71,	72,	73,	72,	73,	74,	73,	74,	75,	74,	75,	76,	75,	76,	77,	76,	77,	78,	77,	78,	79,	78,	79,	80,	79,	80,	81,	80,	81,	82,	81,	82,	83,	82,	83,	84,	83,	84,	85,	84,	85,	86,	85,	86,	87,	86,	87,	88,	87,	88,	89,	88,	89,	90,	89,	90,	91,	90,	91,	92,	91,	92,	93,	92,	93,	94,	93,	94,	95,	94,	95,	96,	95,	96,	97,	96,	97,	98,	97,	98,	99,	98,	99,	100,	99,	100,	101,	};


    unsigned int VBO, VAO, EBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glGenBuffers(1, &EBO);

    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

    // Координатные атрибуты
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void *) 0);
    glEnableVertexAttribArray(0);

    // Цветовые атрибуты
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void *) (3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    // Атрибуты текстурных координат
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void *) (6 * sizeof(float)));
    glEnableVertexAttribArray(2);


    // Загрузка и создание текстуры
    unsigned int texture;
    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_2D,
                  texture); // все последующие GL_TEXTURE_2D-операции теперь будут влиять на данный текстурный объект

    // Установка параметров наложения текстуры
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,
                    GL_REPEAT); // установка метода наложения текстуры GL_REPEAT (стандартный метод наложения)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

    // Установка параметров фильтрации текстуры
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

    // Загрузка изображения, создание текстуры и генерирование мипмап-уровней
    int width, height, nrChannels;
    unsigned char *data = stbi_load("textures/test.jpg", &width, &height, &nrChannels, STBI_rgb_alpha);
    if (data) {
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data);
        glGenerateMipmap(GL_TEXTURE_2D);
    } else {
        std::cout << "Failed to load texture" << std::endl;
    }
    stbi_image_free(data);


    // Цикл рендеринга
    while (!glfwWindowShouldClose(window)) {
        // Обработка ввода
        processInput(window);

        // Рендеринг
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        // Связывание текстуры
        glBindTexture(GL_TEXTURE_2D, texture);

        // Рендеринг ящика
        ourShader.use();
        glBindVertexArray(VAO);
        glDrawElements(GL_TRIANGLES, n_triangles * 3, GL_UNSIGNED_INT, 0);

        // glfw: обмен содержимым front- и back- буферов. Отслеживание событий ввода/вывода (была ли нажата/отпущена кнопка, перемещен курсор мыши и т.п.)
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // Опционально: освобождаем все ресурсы, как только они выполнили свое предназначение
    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteBuffers(1, &EBO);

    // glfw: завершение, освобождение всех выделенных ранее GLFW-реурсов
    glfwTerminate();
    return 0;
}

// Обработка всех событий ввода: запрос GLFW о нажатии/отпускании кнопки мыши в данном кадре и соответствующая обработка данных событий
void processInput(GLFWwindow *window) {
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);
}

// glfw: всякий раз, когда изменяются размеры окна (пользователем или операционной системой), вызывается данная callback-функция
void framebuffer_size_callback(GLFWwindow *window, int width, int height) {
    // Убеждаемся, что окно просмотра соответствует новым размерам окна.
    // Обратите внимание, что высота и ширина будут значительно больше, чем указано, на Retina-дисплеях
    glViewport(0, 0, width, height);
}