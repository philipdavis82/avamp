from core.interfaces.base_interface import BaseInterface
class SimpleLineInterface (BaseInterface):
    """
    Interface for simple line operations.
    This interface defines methods for basic line operations.
    """

    def __init__(self, x, y, x_name="x", y_name="y"):
        """
        Initialize the simple line interface.

        :param x: The x-coordinate or data.
        :param y: The y-coordinate or data.
        :param x_name: Optional name for the x-coordinate.
        :param y_name: Optional name for the y-coordinate.
        """
        super().__init__()
        self._x = x
        self._y = y
        self._x_name = x_name
        self._y_name = y_name
    @property
    def x(self):
        """
        Return the x-coordinate or data.

        :return: The x-coordinate or data.
        """
        return self._x
    
    @property
    def y(self):
        """
        Return the y-coordinate or data.
        :return: The y-coordinate or data.
        """
        return self._y
    