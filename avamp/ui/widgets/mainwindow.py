from avamp.core.logging import LOG
from avamp.core.parsers import PARSERS
from avamp.core.event_manager import EventManager, BuiltInEvents

from avamp.ui.widgets.utility.filebrowser import FileBrowser
from avamp.ui.widgets.utility.datalist    import DataList
from avamp.ui.styles import styles


from PyQt6.QtWidgets import QWidget, QGridLayout, QMenuBar
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui     import QWheelEvent, QKeyEvent
from PyQt6.QtCore    import Qt, QObject

class ScrollCtlEventFilter(QObject):
    def zoomIn(self):
        # app = QApplication.instance()
        new_font = QApplication.font()
        new_font.setPointSize( new_font.pointSize() + 2 )
        new_font.setWeight( int(new_font.pointSize()/4) )
        QApplication.setFont(new_font)
        LOG.debug(f"Zoomed in to font size {new_font.pointSize()}")
        for widget in QApplication.allWidgets():
            widget.setFont(new_font)
            widget.update()
    def zoomOut(self):
        # app = QApplication.instance()
        new_font = QApplication.font()
        new_font.setPointSize( new_font.pointSize() - 2 )
        new_font.setWeight( int(new_font.pointSize()/4) )
        QApplication.setFont(new_font)
        LOG.debug(f"Zoomed out to font size {new_font.pointSize()}")
        for widget in QApplication.allWidgets():
            widget.setFont(new_font)
            widget.update()

    def eventFilter(self, obj, event):
        if isinstance(event, QWheelEvent):
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                # Handle zooming
                if event.angleDelta().y() > 0:
                    LOG.debug("Zooming in")
                    self.zoomIn()
                    # Zoom in logic here
                else:
                    LOG.debug("Zooming out")
                    self.zoomOut()
                    # Zoom out logic here
                return True  # Event handled
            
        elif isinstance(event, QKeyEvent):
            if event.key() == Qt.Key.Key_Plus and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                LOG.debug("Zooming in with Ctrl++")
                self.zoomIn()
                # Zoom in logic here
                return True
            elif event.key() == Qt.Key.Key_Minus and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                LOG.debug("Zooming out with Ctrl+-")
                self.zoomOut()
                # Zoom out logic here
                return True
        return super().eventFilter(obj, event)

class MainWindow(QWidget):
    def __init__(self,roolt_path: str = ""):
        super().__init__()
        self.setWindowTitle("AVAMP")
        self.resize(800, 600)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)   
        self.setLayout(self.layout)

        self.build_menu_bar()
        self.add_file_browser(roolt_path)
        self.add_data_list()

        EventManager.subscribe(BuiltInEvents.VISUAL_READY,self.createVisual)

        self.installEventFilter(ScrollCtlEventFilter(self))
        self.activeWindows = []

    def build_menu_bar(self):
        LOG.debug("Building menu bar")
        self.menue_bar = QMenuBar(self)
        # Here you can add menu items to the menubar
        self.file_menu = self.menue_bar.addMenu("File")
        self.file_menu.addAction("Open")
        self.file_menu.addAction("Save")
        self.file_menu.addAction("Exit", self.close)

        self.view_menu = self.menue_bar.addMenu("View")
        self.view_menu.addAction("Refresh")
        self.view_menu.addAction("Dark Mode",  lambda: QApplication.instance().setStyleSheet(styles.dark()))
        self.view_menu.addAction("Light Mode", lambda: QApplication.instance().setStyleSheet(styles.light()))

        self.help_menu = self.menue_bar.addMenu("Help")
        self.help_menu.addAction("About")
        self.layout.setMenuBar(self.menue_bar)

    def add_file_browser(self, root_path: str = ""):
        LOG.debug(f"Adding file browser with root path: {root_path}")
        self.file_browser = FileBrowser(parent=self, root_path=root_path)
        self.file_browser.filter_by_extension(list(PARSERS.keys()))
        self.layout.addWidget(self.file_browser, 0, 0, 1, 1)
        LOG.info("File browser added to main window layout.")

    def add_data_list(self):
        LOG.debug("Adding data list widget")
        self.data_list = DataList(parent=self)
        self.layout.addWidget(self.data_list, 0, 1, 1, 1)
        LOG.info("Data list added to main window layout.")

    def createVisual(self, visual:object, data:str, filename:str):
        LOG.debug(f"Creating visual for data: {data} from file: {filename}")
        # Placeholder for creating and displaying the visual
        # This could involve creating a new window or embedding in the main window
        window = visual(data=data,filename=filename)
        window.resize(600, 400)
        window.show()
        self.activeWindows.append(window)

    def closeEvent(self, event):
        LOG.debug("Closing main window and all active visual windows.")
        for window in self.activeWindows:
            window.close()
        event.accept()

    def show(self):
        super().show()
        LOG.debug("Main window is now visible.")