
from avamp.ui.visualizers.QtGL import opengl_draw_functions as draw
from avamp.ui.visualizers.QtGL.opengl_drawlist import OglDrawList, OglDrawable


class Sphere (OglDrawable):
    def __init__(self, radius=1.0, userdata=None):
        self.radius     = radius
        self.position   = (0,0,0)
        self.rotation   = (0,0,0)
        self.color      = (0.0, 1.0, 1.0, 1.0)
        self.lines      = False
        self.userdata    = userdata

    def draw(self):
        draw.sphere(self.radius, self.position, self.color, self.rotation, self.lines)

class Cube (OglDrawable):
    def __init__(self, size=1.0, userdata=None):
        self.size = size
        self.position   = (0,0,0)
        self.rotation   = (0,0,0)
        self.color      = (1.0, 0.0, 0.0, 1.0)
        self.lines      = False
        self.userdata    = userdata

    def draw(self):
        draw.cube(self.size, self.position, self.color, self.rotation, self.lines)

        
    
    