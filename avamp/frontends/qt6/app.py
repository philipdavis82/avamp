from avamp.core.logging import LOG
from avamp.frontends.qt6.widgets.mainwindow import MainWindow

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QLoggingCategory
from PyQt6.QtGui import QWindow
import os



def main(root_path: str = ""):
    # Get stylesheet  
    stylesheet = os.path.join(os.path.dirname(__file__),"styles","dark-blue","stylesheet.qss")
    stylesheet_path = os.path.dirname(stylesheet)
    if not os.path.exists(stylesheet):
        LOG.error(f"Stylesheet not found: {stylesheet}")
        return
    
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_Use96Dpi)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL)
    os.environ["QT_SCALE_FACTOR"] = "1.4"

    # Or, enable all debug messages for all categories (less specific)
    # QLoggingCategory.setFilterRules("*.debug=true")

    app = QApplication([])
    app.setApplicationName("Avamp")
    
    
    
    with open(stylesheet, "r") as f:
        stylesheet = f.read()
        stylesheet = stylesheet.replace("url(':/dark-blue/", f"url('{stylesheet_path}{os.path.sep}")
        stylesheet = stylesheet.replace("\\", "/")
        app.setStyleSheet(stylesheet)
    main_window = MainWindow(roolt_path=root_path)
    main_window.setWindowFlags(main_window.windowFlags() | Qt.WindowType.MSWindowsOwnDC | Qt.WindowType.NoTitleBarBackgroundHint | Qt.WindowType.ExpandedClientAreaHint)
    main_window.show()
    app.exec()