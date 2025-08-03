from avamp.core.logging import LOG
from avamp.core.event_manager import EventManager,BuiltInEvents

from PyQt6.QtWidgets import QTreeView, QWidget
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QVBoxLayout



class FileBrowser(QTreeView):
    def __init__(self, parent=None, root_path:str=""):
        super().__init__(parent=parent)
        self.setWindowTitle(type(self).__name__)
        LOG.debug(f"File browser initialized with root path: {root_path}")
        # Set up the file system model
        self.model = QFileSystemModel()
        self.model.setRootPath(root_path)

        # Create a tree view to display the file system
        self.setModel(self.model)
        self.setRootIndex(self.model.index(root_path))
        self.setColumnWidth(0, 250)  # Set the width of the first column

        # Callbacks
        self.doubleClicked.connect(self.on_item_clicked)

    def filter_by_extension(self, extensions: list[str]):
        """Filter the file browser to show only files with the specified extension."""
        # extensions = list(PARSERS.keys())
        filters = []
        for extension in extensions:
            LOG.debug(f"Applying filter for extension: {extension}")
            if not extension.startswith('.'):
                extension = '.' + extension
            filters.append(f"*{extension}")
        self.model.setNameFilters(filters)
        self.model.setNameFilterDisables(False)
    
    def on_item_clicked(self, index):
        """Handle item click events."""
        file_path = self.model.filePath(index)
        LOG.info(f"Item clicked: {file_path}")
        # Here you can add logic to handle the clicked item, e.g., open a file or display its contents
        # For now, we just log the file path
        if self.model.isDir(index):
            LOG.info(f"Directory clicked: {file_path}")
        else:
            LOG.info(f"File clicked: {file_path}")
            EventManager.trigger_event(
                BuiltInEvents.FILE_SELECTED,
                file_path=file_path
            )
            # You can add logic to open the file or perform other actions here
            # For example, you could emit a signal to notify other parts of the application

    
    
        
        
        