#version 330 core
out vec4 FragColor;

in vec3 ourColor;
in vec2 TexCoord;

// Текстурный сэмплер
uniform sampler2D texture1;

void main()
{
    vec4 tex = texture(texture1, TexCoord);
    float grey = (tex.x + tex.y + tex.z) / 3.0;
    FragColor = vec4(grey,grey,grey,1);
}

