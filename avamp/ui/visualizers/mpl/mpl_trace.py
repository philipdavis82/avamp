from avamp.core.interfaces.lines.simple_line_interface import SimpleLineInterface

from matplotlib.lines import Line2D


class MplTrace():
    """
    Stores the line information from matplolib
    """
    _internal: SimpleLineInterface
    _line: Line2D
    _active: bool

    def __init__(self ,line):
        """
        Initialize the mpl trace.

        :param line: The matplotlib line object.
        """
        self._internal = SimpleLineInterface([],[])
        self._line     = line
        self._active   = True
    
    def interface(self) -> SimpleLineInterface:
        """
        Return the interface associated with the trace.

        :return: The SimpleLineInterface associated with the trace.
        """
        return self._internal

    def set_interface(self, interface: SimpleLineInterface):
        """
        Set the interface for the trace.

        :param interface: The interface to set.
        """
        self._internal = interface

    def x_data(self):
        """
        Return the x data of the line.

        :return: The x data of the line.
        """
        return self._line.get_xdata()
    
    def y_data(self):
        """
        Return the y data of the line.

        :return: The y data of the line.
        """
        return self._line.get_ydata()
    
    def set_x_data(self, x):
        """
        Set the x data of the line.

        :param x: The new x data.
        """
        self._line.set_xdata(x)
    
    def set_y_data(self, y):
        """
        Set the y data of the line.

        :param y: The new y data.
        """
        self._line.set_ydata(y)
    
    def draw_floating_numbers(self):
        """
        Draw floating point numbers on the line.
        """
        for x, y in zip(self.x_data(), self.y_data()):
            self._line.axes.text(x, y, f"{y:.2f}", fontsize=8)