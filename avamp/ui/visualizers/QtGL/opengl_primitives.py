import numpy as np

class Transformation:
    def __init__(self, position=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0)):
        self.matrix = self.get_matrix(position, rotation, scale)

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
        