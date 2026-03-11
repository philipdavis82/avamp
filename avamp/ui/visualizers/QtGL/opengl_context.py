import sys
from PySide6.QtCore import Qt, QObject, QEvent
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QSurfaceFormat
from OpenGL.GL import *
from OpenGL.GLU import *

try:
    import opengl_drawlist
except ImportError:
    from avamp.ui.visualizers.QtGL import opengl_drawlist

# Add scroll event handling for zooming
class ScrollMouseEvent(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            # print(f"Zooming with scroll {event.angleDelta().y()}")
            delta = event.angleDelta().y()
            obj.zoom(delta)
            return True
        return super().eventFilter(obj, event)

class GlWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drawlist = opengl_drawlist.OglDrawList()

    def initializeGL(self):
        """Initialize OpenGL state, lighting, and textures."""
        glEnable(GL_DEPTH_TEST) # Handle overlapping objects
        glEnable(GL_LIGHTING)   # Enable lighting
        glEnable(GL_LIGHT0)     # Use light 0
        glEnable(GL_COLOR_MATERIAL)
        
        # Enable alpha blending for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Set Clipping planes for better depth handling
        glEnable(GL_CLIP_PLANE0)
        
        self.currPosition = 0,0
        self.lastPos = 0,0
        self.rotationX = 0
        self.rotationY = 0
        self.currentZoom = -10.0
        self.fov = 60.0
        # Simple light setup
        glLightfv(GL_LIGHT0, GL_POSITION, (100.0, 100.0, 100.0, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
        glClipPlane(GL_CLIP_PLANE0, (0.0, 0.0, -1.0, 0.0)) # Clip everything behind the camera
        glClipPlane(GL_CLIP_PLANE1, (0.0, 0.0, 1.0, -1000.0)) # Clip everything too far away
        
        glClearColor(1.0, 1.0, 1.0, 1.0) # Black background
        glDepthMask(GL_TRUE)

        #install event filter for scroll events
        self.installEventFilter(ScrollMouseEvent(self))


    # Add Turntable functionality
    def mousePressEvent(self, event):
        self.lastPos = event.position()
    
    def mouseMoveEvent(self, event):
        self.currPosition = event.position()
        dx = self.currPosition.x() - self.lastPos.x()
        dy = self.currPosition.y() - self.lastPos.y()
        self.rotationX += dy * 0.5
        self.rotationY += dx * 0.5
        self.lastPos = self.currPosition
        self.update() # Trigger a repaint
    
    def mouseReleaseEvent(self, event):
        pass # No action needed on release for now

    def zoom(self, delta):
        self.currentZoom += (delta / 120.0) * self.currentZoom/4.0 # Adjust zoom based on scroll delta
        self.currentZoom = max(-100.0, min(-2.0, self.currentZoom)) # Clamp zoom to reasonable range
        self.update() # Trigger a repaint
    
    def cameraTransform(self):
        # Transform based on mouse movement for a simple turntable effect
        glTranslatef(0.0, 0.0, self.currentZoom) # Move back to see the object
        glRotatef(self.rotationX, 1.0, 0.0, 0.0) # Rotate around X-axis
        glRotatef(self.rotationY, 0.0, 1.0, 0.0) # Rotate around Y-axis

    def resizeGL(self, w, h):
        """Handle window resizing."""
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, w / h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
   
    def paintGL(self):
        """Render the scene."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glClearColor(1.0, 1.0, 1.0, 1.0)
        glLoadIdentity()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # Reset to fill mode
        
        self.cameraTransform() 
        
        self.drawlist.draw() # Render all drawables in the draw list
        
        


if __name__ == "__main__":
    import opengl_draw_functions as draw
    class MainWindow(QMainWindow):
        def __init__(self,glc):
            super().__init__()
            self.setWindowTitle("PySide6 OpenGL Sphere")
            self.setCentralWidget(glc)
            self.resize(800, 600)
    app = QApplication(sys.argv)
    glc = GlWidget()
    window = MainWindow(glc)
    glc.drawlist.add_drawable_function(draw.cube ,4, position=(0,0,0),lines=True) # Draw the red cube first
    glc.drawlist.add_drawable_function(draw.sphere ,1.0, position=(0,0,0), color=(0.0, 1.0, 1.0, .2)) # Draw the semi-transparent cyan sphere
    window.show()
    sys.exit(app.exec())