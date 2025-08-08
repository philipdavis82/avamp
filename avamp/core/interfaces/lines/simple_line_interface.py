from avamp.core.interfaces.base_interface import BaseInterface
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

    def type(self) -> str:
        """
        Return the type of the interface.

        :return: The type of the interface.
        """
        return "line"
    
    def name(self) -> str:
        """
        Return the name of the interface.

        :return: The name of the interface.
        """
        return self.__class__.__name__

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
    
    def serialize(self) -> str:
        """
        Serializes data to a csv string.
        """
        lines = [f"{self._x_name},{self._y_name}"]
        for x, y in zip(self._x, self._y):
            lines.append(f"{x},{y}")
        return "\n".join(lines)
    
    def deserialize(self, data):
        """
        Deserializes data from a csv string.
        """
        lines = data.strip().split("\n")
        header = lines[0].split(",")
        self._x_name = header[0]
        self._y_name = header[1]
        x, y = [], []
        for line in lines[1:]:
            values = line.split(",")
            x.append(float(values[0]))
            y.append(float(values[1]))
        self._x = x
        self._y = y
        