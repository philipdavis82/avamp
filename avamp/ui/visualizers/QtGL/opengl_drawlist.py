


class OglDrawable:
    def __init__(self,draw,*args,**kwargs):
        self._draw = draw
        self.args = args
        self.kwargs = kwargs
    def draw(self):
        self._draw(*self.args,**self.kwargs)


class OglDrawList:
    def __init__(self):
        self.drawables = []
    
    def add_drawable(self, drawable):
        self.drawables.append(drawable)
    
    def add_drawable_function(self, func, *args, **kwargs):
        self.drawables.append(OglDrawable(func, *args, **kwargs))
    
    def draw(self):
        for drawable in self.drawables:
            drawable.draw()