from avamp.core.logging import LOG
from avamp.core.dispatcher import VisualDispatcher

from avamp.ui.plotting.mpl.mpl_canvas import MplCanvas

from PyQt6.QtWidgets import QWidget, QGridLayout

class LineMpl(QWidget):
    def __init__(self, data , filename , parent=None, width=5, height=4, dpi=100):
        super().__init__(parent)
        self.setWindowTitle(f"Line Plot - {data.name()} ({filename})")

        self._layout = QGridLayout(self)
        self.setLayout(self._layout)

        self.canvas = MplCanvas(self, width, height, dpi)
        self.navbar = self.canvas.navbar()

        self.canvas.axes.set_title("Line Plot")
        self.canvas.axes.set_xlabel(data._x_name)
        self.canvas.axes.set_ylabel(data._y_name)
        self.plot(data.x, data.y)

        self._layout.addWidget(self.canvas, 0, 0)
        self._layout.addWidget(self.navbar, 1, 0)

        LOG.debug(f"LineMpl visualizer created for {data.name()} from {filename}")
        
    def plot(self, x, y):
        self.canvas.axes.clear()
        self.canvas.axes.plot(x, y)
        self.canvas.draw()
    
    
VisualDispatcher.add_visual(LineMpl, "line")