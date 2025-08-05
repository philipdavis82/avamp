
from PyQt6.QtWidgets import QApplication, QWidget

from matplotlib.backends.backend_qtagg  import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure                  import Figure


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
    
    def navbar(self):
        self.toolbar = NavigationToolbar(self, self)
        return self.toolbar