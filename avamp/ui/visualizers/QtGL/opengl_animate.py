from avamp.ui.visualizers.QtGL.opengl_shapes import Sphere, Cube

class AnimationPoint:
    def __init__(self, timestamp):
        self.timestamp = timestamp

class AnimationPositionPoint(AnimationPoint):
    def __init__(self, timestamp, position):
        super().__init__(timestamp)
        self.position = position

class AnimationRotationPoint(AnimationPoint):
    def __init__(self, timestamp, rotation):
        super().__init__(timestamp)
        self.rotation = rotation

class AnimationColorPoint(AnimationPoint):
    def __init__(self, timestamp, color):
        super().__init__(timestamp)
        self.color = color

class AnimationScalePoint(AnimationPoint):
    def __init__(self, timestamp, scale):
        super().__init__(timestamp)
        self.scale = scale

class AnimatedSphere(Sphere):
    def __init__(self, radius=1.0, userdata=None):
        super().__init__(radius, userdata)

    def update(self):

    def draw(self):
        # Update the position based on the angle
        # self.position = (5 * cos(self.angle), 0, 5 * sin(self.angle))
        # self.angle += 0.01  # Increment the angle for animation
        super().draw()