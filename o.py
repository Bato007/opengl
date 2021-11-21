import pygame
import numpy
from OpenGL.GL import *
from OpenGL.GL.shaders import *

pygame.init()
screen = pygame.display.set_mode((1200, 720), pygame.OPENGL | pygame.DOUBLEBUF)
glClearColor(0.1, 0.2, 0.5, 1.0)

# Opengl
vertex_shader = """
#version 460
layout (location = 0) in vec3 position;

void main()
{
    gl_Position = vec4(position.x, position.y, position.z, 1);
}
"""

fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;

void main()
{
    fragColor = vec4(1.0f, 0.5f, 0.5f, 1.0f);
}
"""

# Compilando los shaders
# Compiled ${name} shader
cvs = compileShader(vertex_shader, GL_VERTEX_SHADER)
cfs = compileShader(fragment_shader, GL_FRAGMENT_SHADER)

shader = compileProgram(cvs, cfs)

vertex_data = numpy.array([
    -1, -1, 0,
    1, -1, 0,
    0, 1, 0
], dtype=numpy.float32)

# Se aparta un bloque de memoria, se activa y se mete
vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

# Sirve para describir la data
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)
glVertexAttribPointer(
    0, # Location
    3, # Cada cuantos del array son un objeto
    GL_FLOAT, # Tipo de datos
    GL_FALSE, # normalizados ?
    4 * 3, # Stride
    ctypes.c_void_p(0), # Desde donde empieza la data
)
glEnableVertexAttribArray(0)

running = True
while running:
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader)
    glDrawArrays(GL_TRIANGLES, 0, 3)

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        # Para las teclas
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_w:
                pass
            if event.type == pygame.K_d:
                pass
            if event.type == pygame.K_s:
                pass
            if event.type == pygame.K_a:
                pass