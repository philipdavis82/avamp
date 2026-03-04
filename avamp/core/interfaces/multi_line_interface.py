from avamp.core.interfaces.base_interface import BaseInterface
from avamp.core.interfaces.simple_line_interface import SimpleLineInterface

class MultiLineInterface (BaseInterface):
    def __init__(self, lines: list[SimpleLineInterface]):
        self._lines = lines

    
    def type(self) -> str:
        """
        Return the type of the interface.

        :return: The type of the interface.
        """
        return "multi_line"
    
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
        return [line.x for line in self._lines]
    
    @property
    def y(self):
        """
        Return the y-coordinate or data.
        :return: The y-coordinate or data.
        """
        return [line.y for line in self._lines]
    
    def serialize(self) -> str:
        """
        Serializes data to a csv string.
        """
        lines = []
        for line in self._lines:
            lines.append(f"{line._x_name},{line._y_name}")
            for x, y in zip(line.x, line.y):
                lines.append(f"{x},{y}")
        return "\n".join(lines)
    
    def deserialize(self, data):
        """
        Deserializes data from a csv string.
        """
        lines = data.strip().split("\n")
        self._lines = []
        current_line = None
        for line in lines:
            if ',' in line:
                x_name, y_name = line.split(',')
                current_line = SimpleLineInterface([], [], x_name, y_name)
                self._lines.append(current_line)
            else:
                x, y = line.split(',')
                if current_line is not None:
                    current_line._x.append(float(x))
                    current_line._y.append(float(y))
        
        
    
