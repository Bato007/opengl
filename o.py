import pygame
import numpy
import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import *

width, height = 1200, 720
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
glClearColor(0.1, 0.2, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)
clock = pygame.time.Clock()

# Opengl
vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 ccolor;

uniform mat4 theMatrix;

out vec3 mycolor;

void main()
{
    gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1);
    mycolor = ccolor;
}
"""

fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;
in vec3 mycolor;

void main()
{
    fragColor = vec4(mycolor, 1.0f);
}
"""

# Compilando los shaders
# Compiled ${name} shader
cvs = compileShader(vertex_shader, GL_VERTEX_SHADER)
cfs = compileShader(fragment_shader, GL_FRAGMENT_SHADER)

shader = compileProgram(cvs, cfs)

vertex_data = numpy.array([
    0.5,  0.5, 0.5, 1.0, 0.2, 0.2, # top right  front  0
    0.5, -0.5, 0.5, 1.0, 0.2, 0.2, # bottom right front 1
    -0.5, -0.5,  0.5, 1.0, 0.2, 0.2, # bottom left front 2
    -0.5,  0.5,  0.5, 1.0, 0.2, 0.2, # top left front 3
    0.5,  0.5, -0.5, 0.2, 1.0, 0.2, # top right  back 4
    0.5, -0.5, -0.5, 0.2, 1.0, 0.2, # bottom right back 5
    -0.5, -0.5,  -0.5, 0.2, 1.0, 0.2, # bottom left back 6
    -0.5,  0.5,  -0.5, 0.2, 1.0, 0.2, # top left back 7
], dtype=numpy.float32)

index_data = numpy.array([
    1, 2, 3, 0, 1, 3, # Front
    5, 6, 7, 4, 5, 7, # Back
    0, 3, 4, 7, 4, 3, # top
    1, 2, 5, 6, 5, 2, # bottom
    0, 1, 4, 5, 4, 1, # right
    2, 3, 6, 7, 6, 3, # left
], dtype=numpy.uint32)

# Se aparta un bloque de memoria, se activa y se mete
vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

# Sirve para describir la data
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)
# Para los vertices
glVertexAttribPointer(
    0, # Location
    3, # Cada cuantos del array son un objeto
    GL_FLOAT, # Tipo de datos
    GL_FALSE, # normalizados ?
    4 * 6, # Stride
    ctypes.c_void_p(0), # Desde donde empieza la data
)
glEnableVertexAttribArray(0)

# Ahora es para los index
element_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

# Para los colores
glVertexAttribPointer(
    1, # Location
    3, # Cada cuantos del array son un objeto
    GL_FLOAT, # Tipo de datos
    GL_FALSE, # normalizados ?
    4 * 6, # Stride
    ctypes.c_void_p(12), # Desde donde empieza la data
)
glEnableVertexAttribArray(1)

glUseProgram(shader)

Identity = glm.mat4(1)

def render(a):
    Traslate = glm.translate(Identity, glm.vec3(0, 0, 0))
    Rotate = glm.rotate(Identity, 0, glm.vec3(0, 1, 0))
    Scale = glm.scale(Identity, glm.vec3(1, 1, 1))
    Model = Traslate * Rotate * Scale

    View = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, glm.radians(a), 0), glm.vec3(0, 1, 0))
    Projection = glm.perspective(glm.radians(45), width/height, 0.1, 1000.0)

    theMatrix = Projection * View * Model

    glUniformMatrix4fv(
        glGetUniformLocation(shader, 'theMatrix'),
        1,
        GL_FALSE,
        glm.value_ptr(theMatrix)
    )

glViewport(0, 0, width, height)
a = 0
running = True
while running:
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    render(a)
    a += 1
    glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)
    
    pygame.display.flip()
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        # Para las teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pass
            if event.key == pygame.K_d:
                pass
            if event.key == pygame.K_s:
                glPolygonMode(GL_FRONT_AND_BACK, GL_TRIANGLES)
            if event.key == pygame.K_a:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)