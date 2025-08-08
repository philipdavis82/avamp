
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QObject, QEvent, Qt
from PyQt6.QtGui import QWheelEvent, QKeyEvent


from matplotlib.backends.backend_qtagg  import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure                  import Figure


class CtlEventFilter(QObject):
    def eventFilter(self, obj, event):
        if isinstance(event, QWheelEvent):
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                if event.angleDelta().y() > 0:
                    obj.zoomIn()
                else:
                    obj.zoomOut()
                return True
        return super().eventFilter(obj, event)


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        
        self.dpi = self.figure.get_dpi()

        self.setParent(parent)
        self.installEventFilter(CtlEventFilter(self))
        

    def navbar(self):
        self.toolbar = NavigationToolbar(self, self)
        return self.toolbar
    
    def zoomIn(self):
        self.dpi += 10
        self.figure.set_dpi(self.dpi)
        self.resize(int(self.width() * self.dpi / 100), int(self.height() * self.dpi / 100))
        self.draw()
        self.flush_events()
        self.figure.canvas.flush_events()
        self.figure.canvas.updateGeometry()
        self.update()
        QApplication.processEvents()
        
    def zoomOut(self):
        self.dpi -= 10 if self.dpi > 10 else 0
        if self.dpi < 10:
            self.dpi = 10
        self.figure.set_dpi(self.dpi)
        self.resize(int(self.width() * self.dpi / 100), int(self.height() * self.dpi / 100))
        self.draw()
        self.flush_events()
        self.figure.canvas.flush_events()
        self.figure.canvas.updateGeometry()
        self.update()
        QApplication.processEvents()
