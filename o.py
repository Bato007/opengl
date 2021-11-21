import pygame
import numpy
from OpenGL.GL import *

pygame.init()
screen = pygame.display.set_mode((1200, 720), pygame.OPENGL | pygame.DOUBLEBUF)

# Opengl
glClearColor(0.5, 1.0, 0.5, 1.0)
vertex_data = numpy.array([
    -1, -1, 0,
    1, -1, 0,
    0, -1, 0
], dtype=numpy.float32)

running = True
while running:
    glClear(GL_COLOR_BUFFER_BIT)
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