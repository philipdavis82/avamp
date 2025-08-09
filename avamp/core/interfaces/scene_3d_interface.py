from avamp.core.logging import LOG
from avamp.core.interfaces.base_interface import BaseInterface

class Scene3DInterface(BaseInterface):
    class Object3D:
        class ShapeSphere:
            """
            Represents a circle shape in 3D space.
            """
            def __init__(self, radius: float = 1.0):
                self.radius = radius
        class ShapeCube:
            """
            Represents a cube shape in 3D space.
            """
            def __init__(self, width: float = 1.0, height: float = 1.0, depth: float = 1.0):
                self.width = width
                self.height = height
                self.depth = depth

        """
        Represents a 3D object in the scene.
        """
        def __init__(self, name: str, position: list[tuple], rotation: list[tuple], scale: list[tuple]):
            self.name       = name
            self.position   = position # list of 3D coordinates (x, y, z)
            self.rotation   = rotation # list of 3x3 rotation matricies
            self.scale      = scale    # list of 3D scale factors (sx, sy, sz)
            self.visible    = []
            self.shape      = None
            self.color      = None
            self.material   = None
            self.mesh       = None  # Placeholder for mesh data
            self.instances  = []  # Placeholder for instances of the object, non zero if the object is instanced
        
        def create_instance(self) -> list[list[float]]:
            """
            Create an instance of the 3D object.
            
            :return: A list representing the instance data.
            """
            return [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]  # Identity matrix as a placeholder

        def set_shape(self, shape: str,*args, **kwargs):
            """
            Set the shape of the 3D object.

            :param shape: The shape type (e.g., 'sphere', 'cube').
            """
            if shape == 'sphere':
                self.shape = self.ShapeSphere(*args, **kwargs)
            elif shape == 'cube':
                self.shape = self.ShapeCube(*args, **kwargs)
            else:
                LOG.error(f"Unknown shape type: {shape}")
        
    """
    Interface for 3D scene operations.
    This interface defines methods for basic 3D scene operations.
    """

    def __init__(self, objects=None):
        """
        Initialize the 3D scene interface.

        :param objects: Optional list of objects in the 3D scene.
        """
        super().__init__()
        self._objects = objects if objects is not None else []

    def type(self) -> str:
        """
        Return the type of the interface.

        :return: The type of the interface.
        """
        return "3d_scene"
    
    def name(self) -> str:
        """
        Return the name of the interface.

        :return: The name of the interface.
        """
        return self.__class__.__name__
    
    def create_object(self) -> Object3D:
        """
        Add an object to the 3D scene.

        :param obj: The Object3D instance to add.
        """
        obj = self.Object3D(name="New Object", position=[(0, 0, 0)], rotation=[(0, 0, 0)], scale=[(1, 1, 1)])
        self._objects.append(obj)
        return obj
    