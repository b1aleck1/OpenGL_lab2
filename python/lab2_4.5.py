#!/usr/bin/env python3
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(1.0, 1.0, 1.0, 1.0)


def shutdown():
    pass


def draw_rectangle(x, y, a, b):
    half_a = a / 2.0
    half_b = b / 2.0

    v1 = (x - half_a, y - half_b)
    v2 = (x + half_a, y - half_b)
    v3 = (x + half_a, y + half_b)
    v4 = (x - half_a, y + half_b)

    glBegin(GL_TRIANGLES)

    # TRÓJKĄT 1
    glVertex2f(v1[0], v1[1])
    glVertex2f(v2[0], v2[1])
    glVertex2f(v3[0], v3[1])

    # TRÓJKĄT 2
    glVertex2f(v1[0], v1[1])
    glVertex2f(v3[0], v3[1])
    glVertex2f(v4[0], v4[1])

    glEnd()

MAX_RECURSION_LEVEL = 5
SIZE = 180.0  # Stała wielkość początkowa Dywanu Sierpińskiego (180x180)

def draw_sierpinski_carpet(x, y, a, b, level):
    if level == 0:
        glColor3f(0.8, 0.4, 0.0)
        draw_rectangle(x, y, a, b)
        return

    new_a = a / 3.0
    new_b = b / 3.0
    new_level = level - 1

    for i in range(3):
        for j in range(3):

            if i == 1 and j == 1:
                continue

            new_x = x + (i - 1) * new_a
            new_y = y + (j - 1) * new_b

            draw_sierpinski_carpet(new_x, new_y, new_a, new_b, new_level)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)  # Przechodzimy do manipulacji modelem
    glLoadIdentity()  # Resetujemy macierz modelu

    # Obliczamy potrzebną skalę.
    # Docelowy zakres: [-100, 100] = 200 jednostek.
    # Aktualny rozmiar fraktala: SIZE = 180 jednostek.
    SCALE_FACTOR = 200.0 / SIZE

    # SKALUJEMY fraktal, aby wypełnił całą rzutnię
    glScalef(SCALE_FACTOR, SCALE_FACTOR, 1.0)

    # Rysowanie Dywanu Sierpińskiego (rozmiar pozostaje 180x180, ale jest skalowany)
    draw_sierpinski_carpet(0.0, 0.0, SIZE, SIZE, MAX_RECURSION_LEVEL)

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Dywan Sierpińskiego (4.5)", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()