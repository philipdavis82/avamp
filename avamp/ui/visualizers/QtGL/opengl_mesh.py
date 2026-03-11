import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

from avamp.ui.visualizers.QtGL.opengl_primitives import Transformation
from avamp.ui.visualizers.QtGL.opengl_drawlist   import OglDrawable

class Mesh(OglDrawable):
    def __init__(self, vertices, faces, color=(0.5, 0.5, 0.5, 1.0), lines=False):
        self.vertices = vertices
        self.faces = faces
        self.color = color
        self.lines = lines
        self.trasformation = Transformation()
        self.vertex_buffer = None
        self.face_buffer   = None

    def createBuffer(self):
        self.vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        vertex_data = np.array(self.vertices, dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

        self.face_buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.face_buffer)
        face_data = np.array(self.faces, dtype=np.uint32)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, face_data.nbytes, face_data, GL_STATIC_DRAW)

    def draw(self):
        if self.vertex_buffer is None or self.face_buffer is None:
            self.createBuffer()
        
        glColor4f(*self.color)
        if self.lines:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        #Transform 
        glPushMatrix()
        if self.trasformation is not None:
            glMultMatrixf(self.trasformation.matrix.T) # OpenGL expects column-major order, so we transpose the matrix

        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glVertexPointer(3, GL_FLOAT, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.face_buffer)
        glDrawElements(GL_TRIANGLES, len(self.faces) * 3, GL_UNSIGNED_INT, None)

        glDisableClientState(GL_VERTEX_ARRAY)
        glPopMatrix()
    
    