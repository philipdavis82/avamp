from OpenGL.GL import *
from OpenGL.GLU import *

def sphere(radius=1.0, position=(0.0, 0.0, 0.0), color=(0.0, 1.0, 1.0, 1.0), rotation=(0.0, 0.0, 0.0), lines=False):
    glPushMatrix()
    glTranslatef(*position) 
    glRotatef(rotation[0], 1.0, 0.0, 0.0) # Rotate around X-axis
    glRotatef(rotation[1], 0.0, 1.0, 0.0) # Rotate around Y-axis
    glRotatef(rotation[2], 0.0, 0.0, 1.0) # Rotate around Z-axis
    glColor4f(*color) # Set color with alpha

    quadric = gluNewQuadric()
    if lines:
        gluQuadricDrawStyle(quadric, GLU_LINE)
    else:
        gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, radius, 16, 16) # Radius, slices, stacks
    gluDeleteQuadric(quadric)
    glPopMatrix()

def cube(size=1.0, position=(0.0, 0.0, 0.0), color=(1.0, 0.0, 0.0, 1.0), rotation=(0.0, 0.0, 0.0), lines=False):
    # def cube(size=1.0, transformation = )
    if(lines):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glColor4f(*color) # Set color with alpha

    glPushMatrix()
    # glTranslatef(*position) 
    # glRotatef(rotation[0], 1.0, 0.0, 0.0) # Rotate around X-axis
    # glRotatef(rotation[1], 0.0, 1.0, 0.0) # Rotate around Y-axis
    # glRotatef(rotation[2], 0.0, 0.0, 1.0) # Rotate around Z-axis
    # glutSolidCube is not available in PyOpenGL, so we can draw a cube manually
    glBegin(GL_QUADS)
    # Front face
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)
    # Back face
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, -size, -size)
    # Left face
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, -size, size)
    glVertex3f(-size, size, size)
    glVertex3f(-size, size, -size)
    # Right face
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(size, -size, size)
    # Top face
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)
    # Bottom face
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(-size, -size, size)
    glEnd()
    glPopMatrix()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # Reset to fill mode