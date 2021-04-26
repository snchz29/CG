#version 430

uniform mat4 projMat;
uniform mat4 viewMat;
uniform mat4 modelMat;
//attribute vec3 position;
//attribute vec3 normal;
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
out vec3 Normal;
out vec3 FragPos;

void main()
{
    FragPos = vec3(modelMat * vec4(vec3(position.x, position.z, position.y), 1.0));
    Normal = vec3(normal.x, normal.z, normal.y);
    //gl_Position = projMat * viewMat * modelMat * vec4(vec3(position.x, position.z, position.y), 1.0);
    gl_Position = projMat * viewMat * modelMat * vec4(vec3(position.x, position.z, position.y), 1.0);
}