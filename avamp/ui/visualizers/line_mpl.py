from avamp.core.logging import LOG
from avamp.core.dispatcher import VisualDispatcher
from avamp.core.interfaces.simple_line_interface import SimpleLineInterface
from avamp.ui.visualizers.mpl.mpl_canvas import MplCanvas
from avamp.ui.visualizers.mpl.mpl_trace  import MplTrace
from PyQt6.QtWidgets import QWidget, QGridLayout,QMenuBar, QMenu, QApplication, QStatusBar, QSizePolicy
from PyQt6.QtCore import QEvent, Qt, QObject
from PyQt6.QtGui import QImage, QContextMenuEvent, QKeyEvent
import os
import io
import base64

class RightClickEventFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.ContextMenu:
            LOG.debug(f"Event: {event} {type(event)}")
            # if event.button() == Qt.MouseButton.RightButton:
            obj.context_menue(event.pos())
            return True
        return super().eventFilter(obj, event)
    
class CtlCopyEventFilter(QObject):
    def eventFilter(self, obj, event):
        if isinstance(event, QKeyEvent):
            if not hasattr(obj, "_debouncer_ctlkey"):
                obj._debouncer_ctlkey = False
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier and not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
                if event.key() == Qt.Key.Key_C:
                    if obj._debouncer_ctlkey == "c": return True
                    obj.copy_to_clipboard()
                    obj._debouncer_ctlkey = "c"
                    return True
                elif event.key() == Qt.Key.Key_V:
                    if obj._debouncer_ctlkey == "v": return True
                    obj.paste_from_clipboard()
                    obj._debouncer_ctlkey = "v"
                    return True
                else:
                    obj._debouncer_ctlkey = False
            elif event.modifiers() & Qt.KeyboardModifier.ControlModifier and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                if event.key() == Qt.Key.Key_C:
                    if obj._debouncer_ctlkey == "sc": return True    
                    obj.copy_image_to_clipboard()
                    obj._debouncer_ctlkey = "sc"
                    return True
                else:
                    obj._debouncer_ctlkey = False
            obj._debouncer_ctlkey = False
        return super().eventFilter(obj, event)

class LineMpl(QWidget):
    def __init__(self, data=None , filename=None , parent=None, width=5, height=4, dpi=100):
        super().__init__(parent)

        self._layout = QGridLayout(self)
        self.setLayout(self._layout)

        self.canvas = MplCanvas(self, width, height, dpi)
        self.navbar = self.canvas.navbar()
        self.createMenuBar()
        self.createStatusBar()

        self._layout.addWidget(self.canvas, 0, 0, 1, 2)
        self._layout.addWidget(self.navbar, 1, 0 , 1, 1)

        self.activePlots = []

        if data:
            self.setWindowTitle(f"Line Plot - {data.name()} ({os.path.split(filename)[-1]})")
            self.initialize_from_interface(data)
            LOG.debug(f"LineMpl visualizer created for {data.name()} from {filename}")
        else:
            LOG.debug("LineMpl visualizer created without data")

        self.installEventFilter(RightClickEventFilter(self))
        self.installEventFilter(CtlCopyEventFilter(self))
    
    def copy_to_clipboard(self):
        """
        Copy the current figure to the clipboard.
        """
        clipboard = QApplication.clipboard()
        clipboard.setText(self.serialize())
        self.status_bar.showMessage("Copied data to clipboard", 2000)

    def paste_from_clipboard(self):
        """
        Paste data from the clipboard and add it to the visualizer.
        """
        clipboard = QApplication.clipboard()
        data = clipboard.text()
        if data:
            self.deserialize(data)
            self.status_bar.showMessage("Pasted data from clipboard", 2000)
        else:
            LOG.warning("Clipboard is empty or does not contain valid data.")
            
    
    def copy_image_to_clipboard(self):
        """
        Copy the current figure as an image to the clipboard.
        """
        clipboard = QApplication.clipboard()
        imgdata = io.BytesIO()
        self.canvas.figure.savefig(imgdata, format='png')
        imgdata.seek(0)  # rewind the data
        # clipboard.setImage(imgdata)
        # create a QImage from the PNG data
        image = QImage()
        image.loadFromData(imgdata.getvalue(), "PNG")
        clipboard.setImage(image)
        LOG.debug(f"Copied image to clipboard {image.size()} {image.format()}")
        self.status_bar.showMessage("Copied image to clipboard", 2000)
        # clipboard.setImage(base64.b64decode(imgdata.getvalue()))

    def context_menue(self, pos):
        """
        Create a context menu for the visualizer.
        
        :param pos: The position of the context menu.
        """
        menu = QMenu(self)
        menu.addAction("Copy", self.copy_to_clipboard)
        menu.addAction("Paste", self.paste_from_clipboard)
        menu.addAction("Copy Image", self.copy_image_to_clipboard)
        menu.addAction("Save", self.navbar.save_figure)
        menu.addAction("Close", self.close)
        menu.exec(self.mapToGlobal(pos))

    def createMenuBar(self):
        self.menu_bar = QMenuBar(self)
        self.file_menu = self.menu_bar.addMenu("File")
        self.file_menu.addAction("Save", self.navbar.save_figure)
        self.file_menu.addAction("Close", self.close)   
        self.layout().setMenuBar(self.menu_bar)

    def createStatusBar(self):
        self.status_bar = QStatusBar(self)
        self.status_bar.setSizeGripEnabled(True)
        self.status_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout().addWidget(self.status_bar, 1, 1, 1, 1)

    def clear(self):
        self.canvas.axes.cla()
        self.canvas.draw()

    def initialize_from_interface(self,interface):
        self.canvas.axes.set_title("Line Plot")
        self.canvas.axes.set_xlabel(interface._x_name)
        self.canvas.axes.set_ylabel(interface._y_name)
        self.canvas.axes.grid(True)
        self.canvas.figure.tight_layout()
        trace = self.plot(interface.x, interface.y, label=interface._y_name)
        trace.set_interface(interface)
        self.activePlots.append(trace)
    
    def add_from_interface(self, interface: SimpleLineInterface):
        """
        Add a new trace to the visualizer from a SimpleLineInterface.
        
        :param interface: The SimpleLineInterface to add.
        """
        if not isinstance(interface, SimpleLineInterface):
            LOG.error("Invalid interface type. Expected SimpleLineInterface.")
            return

        trace = self.plot(interface.x, interface.y, label=interface._y_name)
        trace.set_interface(interface)
        self.activePlots.append(trace)

    def plot(self, x, y, *args, **kwargs) -> MplTrace:
        line = self.canvas.axes.plot(x, y, *args, **kwargs)
        self.canvas.draw()
        return MplTrace(line[0])
    
    def serialize(self) -> str:
        """
        Serialize all active plots to a string.
        """
        if len(self.activePlots) == 0:
            return ""
        lines = [[]]
        # build header
        for line in self.activePlots:
            lines[0].append(line.interface()._x_name)
            lines[0].append(line.interface()._y_name)
        
        data_written = True
        index = 0
        while data_written:
            data_written = False
            for i, line in enumerate(self.activePlots):
                if(i == 0): lines.append([])
                if index < len(line.x_data()):
                    lines[-1].append(line.x_data()[index])
                    lines[-1].append(line.y_data()[index])
                    data_written = True
                else:
                    lines[-1].append("")
                    lines[-1].append("")
            index += 1
        LOG.debug(f"Serialized data: {len(lines)} lines")
        return "\n".join([",".join(map(str, line)) for line in lines])
            
    def deserialize(self, data: str):
        """
        Deserialize data from a string and update the visualizer.
        
        :param data: The serialized data string.
        """
        lines = data.strip().split("\n")
        if len(lines) < 2:
            LOG.error("Not enough data to deserialize.")
            return
        LOG.debug(f"Deserializing data with {len(lines)} lines")
        
        header = lines[0].split(",")
        if len(header) % 2 != 0:
            LOG.error("Header does not contain pairs of x and y names.")
            return
        interfaces = []
        for i in range(0, len(header), 2):
            x_name = header[i].strip()
            y_name = header[i + 1].strip()
            interfaces.append(SimpleLineInterface([], [], x_name, y_name))
        for line in lines[1:]:
            values = line.split(",")
            if len(values) != len(interfaces) * 2:
                LOG.error("Data line does not match header length.")
                continue
            for i in range(len(interfaces)):
                x_value = values[i * 2].strip()
                y_value = values[i * 2 + 1].strip()
                if x_value:
                    interfaces[i]._x.append(float(x_value))
                if y_value:
                    interfaces[i]._y.append(float(y_value))
        for interface in interfaces:
            self.add_from_interface(interface)

    
VisualDispatcher.add_visual(LineMpl, "line")