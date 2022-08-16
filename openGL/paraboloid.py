from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *

def esfera():
    glRotatef(1, 1, 0, 0)
    glBegin(GL_POINTS)
    r0 = -2
    rf = 2
    n = 50

    for i in range(0, n):
        r = i * (rf - r0) / n + r0
        for j in range(0, n):
            theta = (j * pi) / n
            x = r * cos(theta)
            y = r**2
            z = r * sin(theta)
            glVertex3f(x, y, z)
    glEnd()


def desenha():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    esfera()
    glutSwapBuffers()


def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50, timer, 1)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(800, 600)
glutCreateWindow("Paraboloid")
glutDisplayFunc(desenha)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
glClearColor(1.0, 0.0, 0.0, 1.0)
#              fov  aspect Ratio  nearPlane  farPlane
gluPerspective(45, 800.0 / 600.0, 0.1, 100.0)
glTranslatef(0.0, 0.0, -15)
glutTimerFunc(50, timer, 1)
glutMainLoop()