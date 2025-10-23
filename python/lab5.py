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


def draw_triangle(v1, v2, v3):
    # Kolor fraktala (np. Czerwony)
    glColor3f(1.0, 0.0, 0.0)

    glBegin(GL_TRIANGLES)
    glVertex2f(v1[0], v1[1])
    glVertex2f(v2[0], v2[1])
    glVertex2f(v3[0], v3[1])
    glEnd()


MAX_RECURSION_LEVEL_TRIANGLE = 6
def draw_sierpinski_triangle(v1, v2, v3, level):
    # 1. WARUNEK ZATRZYMANIA REKURSJI
    # Jeśli osiągnięto dno, rysujemy najmniejszy trójkąt i kończymy.
    if level == 0:
        draw_triangle(v1, v2, v3)
        return

    # 2. PRZYGOTOWANIE DO PODZIAŁU
    new_level = level - 1

    # Obliczanie punktów środkowych boku (dzielenie trójkąta na 4)
    # Środki są w połowie odległości między wierzchołkami

    # Środek V1-V2 (m1)
    m1 = ((v1[0] + v2[0]) / 2.0, (v1[1] + v2[1]) / 2.0)
    # Środek V2-V3 (m2)
    m2 = ((v2[0] + v3[0]) / 2.0, (v2[1] + v3[1]) / 2.0)
    # Środek V3-V1 (m3)
    m3 = ((v3[0] + v1[0]) / 2.0, (v3[1] + v1[1]) / 2.0)

    # 3. REKURENCYJNE WYWOŁANIA (DLA 3 ZEWNĘTRZNYCH TRÓJKĄTÓW)

    # Trójkąt 1 (Lewy górny narożnik)
    draw_sierpinski_triangle(v1, m1, m3, new_level)

    # Trójkąt 2 (Prawy górny narożnik)
    draw_sierpinski_triangle(m1, v2, m2, new_level)

    # Trójkąt 3 (Dolny narożnik)
    draw_sierpinski_triangle(m3, m2, v3, new_level)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Ustawiamy wierzchołki początkowego trójkąta, który wypełni niemal cały obszar [-100, 100]
    # Używamy transformacji, aby wyśrodkować i idealnie dopasować fraktal do okna.

    # Współrzędne trójkąta bazowego (prawie wypełnia rzutnię 200x200):
    # Wierzchołek lewy: (-95, -82)
    # Wierzchołek prawy: (95, -82)
    # Wierzchołek górny: (0, 93)

    v_base1 = (-95.0, -82.0)
    v_base2 = (95.0, -82.0)
    v_base3 = (0.0, 93.0)

    draw_sierpinski_triangle(v_base1, v_base2, v_base3, MAX_RECURSION_LEVEL_TRIANGLE)

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

    window = glfwCreateWindow(400, 400, "Trójkąt Sierpińskiego (5.0)", None, None)
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