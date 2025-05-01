from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *

from src.core.projection import create_perspective_matrix, create_orthographic_matrix
from src.core.matrix import transpose_matrix
from src.core.object_3d import Object3D


class GLRenderer(QGLWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.object: Object3D or None = None
        self.projection_type = 'perspective'

    def initializeGL(self) -> None:
        glClearColor(0.1, 0.1, 0.1, 1.)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w: int, h: int) -> None:
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self.projection_type == 'perspective':
            matrix = create_perspective_matrix(45, w / h, 0.1, 100)
        else:
            matrix = create_orthographic_matrix(-10, 10, -10, 10, -10, 10)

        transposed = transpose_matrix(matrix)
        glLoadMatrixf(sum(transposed, []))
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslatef(0., 0., -5.)

        if self.object:
            transformed_vertices = self.object.get_transformed_vertices()

            glColor3f(1., 1., 1.)
            glBegin(GL_LINES)
            for edge in self.object.edges:
                v1 = transformed_vertices[edge[0]]
                v2 = transformed_vertices[edge[1]]
                glVertex3f(v1[0], v1[1], v1[2])
                glVertex3f(v2[0], v2[1], v2[2])
            glEnd()

    def set_object(self, obj: Object3D) -> None:
        self.object = obj
        self.update()

    def set_projection(self, projection_type) -> None:
        self.projection_type = projection_type
        self.update()
