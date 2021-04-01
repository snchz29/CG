#version 430
//varying vec4 f_color;

//void main(void) {
//    gl_FragColor = vec4(1,0,0,1);
//}
uniform sampler2D uniformImageCover;
//varying vec2 fTexcoords;
//uniform sampler2D textureObj;
//void main()
//{
//    gl_FragColor = texture2D(textureObj, fTexcoords);
////    gl_FragColor = texture2D(uniformImageCover, gl_FragCoord);
//}
out vec4 fragColor;
void main()
{
    fragColor = texture2D(uniformImageCover, gl_FragCoord);
}