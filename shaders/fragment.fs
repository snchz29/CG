#version 430

uniform vec3 lightPos;
uniform mat4 modelMat;
uniform float ambientStrength;
out vec4 fragColor;
in vec3 Normal;
in vec3 FragPos;

void main()
{
    vec3 lightColor = vec3(1.0, 1.0, 1.0);
    vec3 objectColor = vec3(0.0, 1.0, 0.0);
    //float ambientStrength = 0.15;
    vec3 ambient = ambientStrength * lightColor;
//     vec4 lightPosTm = modelMat * vec4(-5.0, -5.0, -5.0, 1.0);
    vec4 lightPosTm = modelMat * vec4(lightPos, 1.0);
    vec3 lightPosTmp = vec3(lightPosTm.x, lightPosTm.y, lightPosTm.z);
    // Диффузная составляющая
    vec3 norm = normalize(Normal);
    //vec3 lightDir = normalize(lightPos - FragPos);
    vec3 lightDir = normalize(lightPosTmp - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    vec3 result = (ambient + diffuse) * objectColor;
    fragColor = vec4(result, 1.0);
}