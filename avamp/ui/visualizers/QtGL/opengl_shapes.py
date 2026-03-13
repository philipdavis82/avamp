import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

try:
    from avamp.ui.visualizers.QtGL.opengl_mesh import Mesh
except ImportError:
    from opengl_mesh import Mesh

class Sphere(Mesh):
    def __init__(self, radius=1.0, *args, **kwargs):    
        
        # Create a UV sphere mesh
        vertices = []
        faces = []
        stacks = 20
        slices = 20
        for i in range(stacks + 1):
            phi = np.pi * i / stacks
            for j in range(slices + 1):
                theta = 2 * np.pi * j / slices
                x = radius * np.sin(phi) * np.cos(theta)
                y = radius * np.cos(phi)
                z = radius * np.sin(phi) * np.sin(theta)
                vertices.append((x, y, z))
        
        for i in range(stacks):
            for j in range(slices):
                first = i * (slices + 1) + j
                second = first + slices + 1
                faces.append((first, second, first + 1))
                faces.append((second, second + 1, first + 1))

        super().__init__(vertices, faces, *args, **kwargs)
        