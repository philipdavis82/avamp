import numpy as np

class Transformation:
    def __init__(self, position=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0)):
        self.matrix = self.get_matrix(position, rotation, scale)

    @property
    def position(self):
        return self.matrix[0:3, 3]
    
    @position.setter
    def position(self, value):
        self.matrix[0:3, 3] = value

    @property
    def rotation(self):
        # This is a simplified way to extract rotation, it assumes no shearing and uniform scaling
        rx = np.arctan2(self.matrix[2, 1], self.matrix[2, 2])
        ry = np.arctan2(-self.matrix[2, 0], np.sqrt(self.matrix[0, 0]**2 + self.matrix[1, 0]**2))
        rz = np.arctan2(self.matrix[1, 0], self.matrix[0, 0])
        return np.degrees((rx, ry, rz))
    
    @rotation.setter
    def rotation(self, value):
        # This is a simplified way to set rotation, it does not handle all cases (like gimbal lock)
        rx, ry, rz = np.radians(value)
        Rx = np.array([[1, 0, 0],
                       [0, np.cos(rx), -np.sin(rx)],
                       [0, np.sin(rx), np.cos(rx)]])
        
        Ry = np.array([[np.cos(ry), 0, np.sin(ry)],
                       [0, 1, 0],
                       [-np.sin(ry), 0, np.cos(ry)]])
        
        Rz = np.array([[np.cos(rz), -np.sin(rz), 0],
                       [np.sin(rz), np.cos(rz), 0],
                       [0, 0, 1]])
        
        self.matrix[0:3, 0:3] = Rz @ Ry @ Rx @ self.matrix[0:3, 0:3]
    
    @property
    def scale(self):
        # This is a simplified way to extract scale, it assumes no shearing
        sx = np.linalg.norm(self.matrix[0:3, 0])
        sy = np.linalg.norm(self.matrix[0:3, 1])
        sz = np.linalg.norm(self.matrix[0:3, 2])
        return (sx, sy, sz)
    
    @scale.setter
    def scale(self, value):
        if isinstance(value, (int, float)):
            value = (value, value, value)
        sx, sy, sz = value
        S = np.diag([sx, sy, sz, 1])
        self.matrix[0:3, 0:3] = self.matrix[0:3, 0:3] @ S[0:3, 0:3]

    def get_matrix(self, position=None, rotation=None, scale=None):
        """
        Compute the transformation matrix based on position, rotation, and scale.
        
        :return: A 4x4 transformation matrix.
        """
        # Create translation matrix
        T = np.eye(4)
        T[0:3, 3] = position

        # Create rotation matrices for X, Y, Z axes
        rx, ry, rz = np.radians(rotation)
        Rx = np.array([[1, 0, 0, 0],
                       [0, np.cos(rx), -np.sin(rx), 0],
                       [0, np.sin(rx), np.cos(rx), 0],
                       [0, 0, 0, 1]])
        
        Ry = np.array([[np.cos(ry), 0, np.sin(ry), 0],
                       [0, 1, 0, 0],
                       [-np.sin(ry), 0, np.cos(ry), 0],
                       [0, 0, 0, 1]])
        
        Rz = np.array([[np.cos(rz), -np.sin(rz), 0, 0],
                       [np.sin(rz), np.cos(rz), 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

        # Create scale matrix
        S = np.diag([scale[0], scale[1], scale[2], 1])

        # Combine transformations: T * Rz * Ry * Rx * S
        return T @ Rz @ Ry @ Rx @ S
        