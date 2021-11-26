import pygame
import numpy
import glm
from obj import *
from OpenGL.GL import *
from OpenGL.GL.shaders import *

width, height = 1200, 720
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
glClearColor(0.1, 0.2, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)
clock = pygame.time.Clock()
mesh = Obj('./tv.obj')

# Se guardan los arrays
index_data = numpy.array([[vertex[0] - 1 for vertex in face] for face in mesh.faces], dtype=numpy.uint32).flatten()
vertex_data = numpy.hstack((
    numpy.array(mesh.vertices, dtype=numpy.float32),
    numpy.array(mesh.normal, dtype=numpy.float32),
    # numpy.array([[vertex[1] - 1 for vertex in face] for face in mesh.faces], dtype=numpy.float32)
)).flatten()

# Opengl
vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;

uniform mat4 theMatrix;
uniform vec3 light;

out float posy;
out float intensity;
out vec3 normals;

void main()
{
    intensity = dot(normal, normalize(light - position));
    gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1);
    posy = position.y;
    normals = normal;
}
"""

fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;

uniform vec3 color;
uniform int option;

in float posy;
in float intensity;
in vec3 normals;

void main()
{
    if (option == 0)
    {
        vec3 fColor = color;
        if (1.15f < posy)
        {
            fColor = vec3(1.0f, 1.0f, 1.0f);
        }
        else if (1.0f < posy && posy <= 1.15f)
        {
            fColor = vec3(1.0f, 0.8f, 0.8f);
        }
        else if (0.9f < posy && posy <= 1.0f)
        {
            fColor = vec3(0.8f, 1.0f, 0.8f);
        }
        else if (0.8f < posy && posy <= 0.9f)
        {
            fColor = vec3(0.8f, 0.8f, 1.0f);
        }
        else if (0.7f < posy && posy <= 0.8f)
        {
            fColor = vec3(0.8f, 0.8f, 0.8f);
        } 
        else if (0.6f < posy && posy <= 0.7f)
        {
            fColor = vec3(0.6f, 0.6f, 0.6f);
        }
        else if (0.5f < posy && posy <= 0.6f)
        {
            fColor = vec3(0.4f, 0.6f, 0.6f);
        }
        else if (0.4f < posy && posy <= 0.5f)
        {
            fColor = vec3(0.6f, 0.4f, 0.4f);
        }
        else if (0.3f < posy && posy <= 0.4f)
        {
            fColor = vec3(0.6f, 0.6f, 0.4f);
        } 
        else if (0.2f < posy && posy <= 0.3f)
        {
            fColor = vec3(0.4f, 0.4f, 0.4f);
        }
        else if (0.1f < posy && posy <= 0.2f)
        {
            fColor = vec3(0.8f, 0.6f, 0.4f);
        } 
        else if (0.0f < posy && posy <= 0.1f)
        {
            fColor = vec3(0.6f, 0.8f, 0.4f);
        }
        else if (-0.1f < posy && posy <= 0.0f)
        {
            fColor = vec3(0.6f, 0.8f, 0.4f);
        } 
        else 
        {
            fColor = vec3(0.0f, 0.0f, 0.0f);
        }
        vec3 mycolor = fColor * intensity;
        fragColor = vec4(mycolor, 1.0f);
    }
    else if (option == 1)
    {
        float intens = intensity;
        if (0.8f < intensity) 
        {
            intens = 1.0f;
        } 
        else if (0.6f < intensity && intensity <= 0.8f) 
        {
            intens = 0.8f;
        } 
        else if (0.4f < intensity && intensity <= 0.6f) 
        {
            intens = 0.8f;
        } 
        else if (0.2 < intensity && intensity <= 0.4f) 
        {
            intens = 0.4f;
        } 
        else 
        { 
            intens = 0.2f;
        }
        vec3 mycolor = color * intens;
        fragColor = vec4(mycolor, 1.0f);
    } 
    else
    {
        vec3 mycolor = normals * intensity;
        fragColor = vec4(mycolor, 1.0f);
    }
}
"""

# Compilando los shaders
# Compiled ${name} shader
cvs = compileShader(vertex_shader, GL_VERTEX_SHADER)
cfs = compileShader(fragment_shader, GL_FRAGMENT_SHADER)

shader = compileProgram(cvs, cfs)   

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

# Ahora es para los index
element_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

glUseProgram(shader)

Identity = glm.mat4(1)
Scale = glm.scale(Identity, glm.vec3(1, 1, 1))
View = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
Projection = glm.perspective(glm.radians(45), width/height, 0.1, 1000.0)

def render(distance, rotate=(0, 0, 0)):
    Traslate = glm.translate(Identity, glm.vec3(0, 0, distance))
    Rotatex = glm.rotate(Identity, glm.radians(rotate[0]), glm.vec3(1, 0, 0))
    Rotatey = glm.rotate(Identity, glm.radians(rotate[1]), glm.vec3(0, 1, 0))
    Rotatez = glm.rotate(Identity, glm.radians(rotate[2]), glm.vec3(0, 0, 1))
    Model = Traslate * Rotatex * Rotatey * Rotatez * Scale

    theMatrix = Projection * View * Model

    glUniformMatrix4fv(
        glGetUniformLocation(shader, 'theMatrix'),
        1,
        GL_FALSE,
        glm.value_ptr(theMatrix)
    )

glViewport(0, 0, width, height)
rotate = [0, 0, 0]
distance = 0

glUniform3f(
    glGetUniformLocation(shader, 'light'),
    0, 0, 10
)

glUniform3f(
    glGetUniformLocation(shader, 'color'),
    0.85, 0.85, 0.85
)

# Initial render
running = True
option = 0
while running:
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glUniform1i(
        glGetUniformLocation(shader, 'option'),
        option,
    )

    render(distance, rotate)
    glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)

    # Check shader
    pygame.display.flip()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                if (distance < 3): distance += 1
            if event.button == 5:
                distance -= 1

        # Para las teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                rotate[0] += 15
            if event.key == pygame.K_s:
                rotate[0] -= 15
            if event.key == pygame.K_d:
                rotate[1] += 15
            if event.key == pygame.K_a:
                rotate[1] -= 15
            if event.key == pygame.K_q:
                rotate[2] += 15
            if event.key == pygame.K_e:
                rotate[2] -= 15
            if event.key == pygame.K_r:
                option = 0
            if event.key == pygame.K_f:
                option = 1
            if event.key == pygame.K_v:
                option = 2