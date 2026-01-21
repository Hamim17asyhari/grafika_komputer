from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

angle = 0

# ======================
# OBJEK BALOK 3D
# ======================
def balok(p, l, t):
    glBegin(GL_QUADS)

    # Depan
    glVertex3f(0, 0, 0)
    glVertex3f(p, 0, 0)
    glVertex3f(p, t, 0)
    glVertex3f(0, t, 0)

    # Belakang
    glVertex3f(0, 0, -l)
    glVertex3f(p, 0, -l)
    glVertex3f(p, t, -l)
    glVertex3f(0, t, -l)

    # Kiri
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, -l)
    glVertex3f(0, t, -l)
    glVertex3f(0, t, 0)

    # Kanan
    glVertex3f(p, 0, 0)
    glVertex3f(p, 0, -l)
    glVertex3f(p, t, -l)
    glVertex3f(p, t, 0)

    # Atas
    glVertex3f(0, t, 0)
    glVertex3f(p, t, 0)
    glVertex3f(p, t, -l)
    glVertex3f(0, t, -l)

    # Bawah
    glVertex3f(0, 0, 0)
    glVertex3f(p, 0, 0)
    glVertex3f(p, 0, -l)
    glVertex3f(0, 0, -l)

    glEnd()

# ======================
# DISPLAY
# ======================
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Kamera tetap
    gluLookAt(
        8, 6, 15,
        0, 2, 0,
        0, 1, 0
    )

    # ===== LANTAI =====
    glColor3f(0.6, 0.4, 0.2)
    glPushMatrix()
    glScalef(10, 0.1, 10)
    balok(1, 1, 1)
    glPopMatrix()

    # ===== DINDING =====
    glColor3f(0.9, 0.9, 0.9)
    glPushMatrix()
    glTranslatef(0, 0, -10)
    glScalef(10, 5, 0.1)
    balok(1, 1, 1)
    glPopMatrix()

    # ===== MEJA =====
    glColor3f(0.5, 0.3, 0.1)
    glPushMatrix()
    glTranslatef(2, 1, -4)
    glScalef(2, 1, 1)
    balok(1, 1, 1)
    glPopMatrix()

    # ===== KURSI =====
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(2.5, 0.5, -2.5)
    balok(1, 1, 1)
    glPopMatrix()

    glutSwapBuffers()

# ======================
# INISIALISASI
# ======================
def init():
    glClearColor(0.5, 0.7, 1.0, 1)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.3, 1, 100)
    glMatrixMode(GL_MODELVIEW)

# ======================
# MAIN
# ======================
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(900, 600)
glutCreateWindow(b"Mini Scene Ruangan 3D")

init()
glutDisplayFunc(display)
glutIdleFunc(display)
glutMainLoop()
