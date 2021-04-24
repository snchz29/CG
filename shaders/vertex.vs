#version 430

uniform mat4 projMat;
uniform mat4 viewMat;
uniform mat4 modelMat;
attribute vec3 aVert;
//layout (location = 0) in vec3 position;

void main()
{
    gl_Position = projMat * viewMat * modelMat * vec4(aVert, 1.0);
    //gl_Position = viewMat * modelMat * vec4(aVert, 1.0);
    //gl_Position = modelMat * vec4(aVert, 1.0);
}