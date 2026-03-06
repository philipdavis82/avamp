from avamp.ui.visualizers.QtGL.opengl_drawlist import OglDrawList,OglDrawable




class GLScene:
    def __init__(self):
        self.objects  = []
        self.drawlist = OglDrawList()

    def add_object(self, obj):
        self.objects.append(obj)
        self.drawlist.add_drawable(obj)
    