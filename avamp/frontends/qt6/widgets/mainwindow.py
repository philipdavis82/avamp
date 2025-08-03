from avamp.core.logging import LOG
from avamp.frontends.qt6.widgets.filebrowser import FileBrowser
from avamp.core.parsers import PARSERS

from PyQt6.QtWidgets import QWidget, QGridLayout, QMenuBar



class MainWindow(QWidget):
    def __init__(self,roolt_path: str = ""):
        super().__init__()
        self.setWindowTitle("VAMP Main Window")
        self.resize(800, 600)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)   
        self.setLayout(self.layout)

        
        self.build_menu_bar()
        self.add_file_browser(roolt_path)

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

        self.help_menu = self.menue_bar.addMenu("Help")
        self.help_menu.addAction("About")
        self.layout.setMenuBar(self.menue_bar)

    def add_file_browser(self, root_path: str = ""):
        LOG.debug(f"Adding file browser with root path: {root_path}")
        self.file_browser = FileBrowser(parent=self, root_path=root_path)
        self.file_browser.filter_by_extension(list(PARSERS.keys()))
        self.layout.addWidget(self.file_browser, 0, 0, 1, 1)
        LOG.info("File browser added to main window layout.")

    def show(self):
        super().show()
        print("Main window is now visible.")