#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;

out vec3 ourColor;
out vec2 TexCoord;

void main()
{
    float pi = 3.1415;
    vec3 bPos = vec3(aPos.x, sin(4*pi*aPos.x)*0.2+aPos.y, 0);
	gl_Position = vec4(bPos, 1.0);
	ourColor = aColor;
	TexCoord = vec2(aTexCoord.x, aTexCoord.y);
}