from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

rotX, rotY = 20, 30  # ángulos de rotación iniciales

def init():
    glClearColor(0.05, 0.05, 0.1, 1.0)  # fondo oscuro
    glEnable(GL_DEPTH_TEST)
    glColor3f(0.9, 0.3, 0.3)  # color de la malla (rojo claro)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -3.0)
    glRotatef(rotX, 1.0, 0.0, 0.0)
    glRotatef(rotY, 0.0, 1.0, 0.0)

    glutWireSphere(1.0, 30, 30)  # esfera en malla
    glutSwapBuffers()

def reshape(w, h):
    if h == 0: h = 1
    aspect = w / h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, aspect, 1.0, 10.0)
    glMatrixMode(GL_MODELVIEW)

def special_keys(key, x, y):
    global rotX, rotY
    if key == GLUT_KEY_UP:
        rotX = (rotX - 5) % 360
    elif key == GLUT_KEY_DOWN:
        rotX = (rotX + 5) % 360
    elif key == GLUT_KEY_LEFT:
        rotY = (rotY - 5) % 360
    elif key == GLUT_KEY_RIGHT:
        rotY = (rotY + 5) % 360
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"Esfera 3D en Malla - OpenGL")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutSpecialFunc(special_keys)
    glutMainLoop()

if __name__ == "__main__":
    main()
