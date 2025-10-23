#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


COLOR1 = (0.0, 0.0, 0.0)
COLOR2 = (0.0, 0.0, 0.0)

# Ustalony kąt obrotu i skalowanie
RANDOM_ANGLE = 0.0
SCALE_X = 1.0
SCALE_Y = 1.0

# Czas ostatniej aktualizacji losowych właściwości (inicjalizowany na 0.0)
LAST_UPDATE_TIME = 0.0
UPDATE_INTERVAL = 1.0  # Interwał zmiany w sekundach

# Parametry bazowego prostokąta
RECT_X, RECT_Y, RECT_A, RECT_B = 0.0, 0.0, 150.0, 100.0


def update_random_properties():
    global COLOR1, COLOR2, RANDOM_ANGLE, SCALE_X, SCALE_Y

    COLOR1 = (random.random(), random.random(), random.random())
    COLOR2 = (random.random(), random.random(), random.random())

    # Losowy Kąt Obrotu (0 do 360 stopni)
    RANDOM_ANGLE = random.uniform(0.0, 360.0)

    # Losowe Przeskalowanie (od 0.7 do 1.3 dla stabilności kształtu)
    SCALE_X = random.uniform(0.7, 1.3)
    SCALE_Y = random.uniform(0.7, 1.3)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # Wywołanie inicjujące przy starcie (pierwszy losowy zestaw)
    update_random_properties()


def shutdown():
    pass


def draw_base_rectangle(x, y, a, b, color1, color2):
    half_a = a / 2.0
    half_b = b / 2.0

    v1 = (x - half_a, y - half_b)
    v2 = (x + half_a, y - half_b)
    v3 = (x + half_a, y + half_b)
    v4 = (x - half_a, y + half_b)

    glBegin(GL_TRIANGLES)

    # TRÓJKĄT 1
    glColor3f(color1[0], color1[1], color1[2])
    glVertex2f(v1[0], v1[1])
    glVertex2f(v2[0], v2[1])
    glVertex2f(v3[0], v3[1])

    # TRÓJKĄT 2
    glColor3f(color2[0], color2[1], color2[2])
    glVertex2f(v1[0], v1[1])
    glVertex2f(v3[0], v3[1])
    glVertex2f(v4[0], v4[1])

    glEnd()


def render(time):
    global LAST_UPDATE_TIME


    # Sprawdzenie, czy minęła co najmniej jedna sekunda od ostatniej aktualizacji
    if time - LAST_UPDATE_TIME >= UPDATE_INTERVAL:
        update_random_properties()
        LAST_UPDATE_TIME = time  # Zaktualizuj czas ostatniego losowania


    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Zastosowanie losowych transformacji (które zmieniają się co sekundę)
    glTranslatef(RECT_X, RECT_Y, 0.0)
    glScalef(SCALE_X, SCALE_Y, 1.0)
    glRotatef(RANDOM_ANGLE, 0.0, 0.0, 1.0)

    draw_base_rectangle(0.0, 0.0, RECT_A, RECT_B, COLOR1, COLOR2)

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

    window = glfwCreateWindow(400, 400, "Losowy 'prostokąt' (4.0)", None, None)
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