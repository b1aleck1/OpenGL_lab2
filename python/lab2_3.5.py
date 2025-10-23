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

# FUNKCJA RYSUJĄCA PROSTOKĄT Z DWÓCH TRÓJKĄTÓW RÓŻNYCH KOLORÓW
def draw_rectangle(x, y, a, b):
    # Obliczamy połowy długości boków
    half_a = a / 2.0
    half_b = b / 2.0

    # Obliczamy współrzędne wierzchołków względem środka (x, y)
    v1 = (x - half_a, y - half_b)  # Lewy dolny
    v2 = (x + half_a, y - half_b)  # Prawy dolny
    v3 = (x + half_a, y + half_b)  # Prawy górny
    v4 = (x - half_a, y + half_b)  # Lewy górny

    glBegin(GL_TRIANGLES)

    # TRÓJKĄT 1: V1, V2, V3 (Dolny-Prawy trójkąt)
    # Kolor Czerwony
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(v1[0], v1[1])
    glVertex2f(v2[0], v2[1])
    glVertex2f(v3[0], v3[1])

    # TRÓJKĄT 2: V1, V3, V4 (Górny-Lewy trójkąt)
    # Kolor Niebieski
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(v1[0], v1[1])
    glVertex2f(v3[0], v3[1])
    glVertex2f(v4[0], v4[1])

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    # Używam jednego wywołania, które rysuje jeden prostokąt,
    # który jest podzielony na dwa trójkąty o różnych kolorach.
    draw_rectangle(0.0, 0.0, 150.0, 100.0)

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

    window = glfwCreateWindow(400, 400, "Prostokąt - różne kolory (3.5)", None, None)
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