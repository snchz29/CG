#version 430
//in vec4 vPosition;
//in float time;
//void main()
//{
//    vec4 temp = vPosition;
//    temp.y = cos(0.1*time)*temp.y;
//    gl_Position = temp;
//}
//attribute vec2 position;
//uniform sampler2D uniformImageCover;
attribute vec2 vPosition;
attribute vec2 vTexcoords;

varying vec2 fTexcoords;
void main()
{
    gl_Position = vec4(vPosition.x/1.33, vPosition.y, 0.0, 1.0);
    fTexcoords = vTexcoords;
    //gl_Position = vec4(position.x, .3 * sin(20.0 * position.x), .3 * cos(20 * position.x), 1.);
}