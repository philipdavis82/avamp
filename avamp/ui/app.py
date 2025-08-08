from avamp.core.logging          import LOG
from avamp.ui.widgets.mainwindow import MainWindow
from avamp.ui.styles             import styles
from avamp.ui                    import visualizers  # Ensure visualizers are registered
from avamp.ui.assets             import assets

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore    import Qt, QLoggingCategory
from PyQt6.QtGui     import QWindow,QFont,QFontDatabase

import os

def main(root_path: str = ""):
    # Get stylesheet  
    
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_Use96Dpi)

    # Or, enable all debug messages for all categories (less specific)
    # QLoggingCategory.setFilterRules("*.debug=true")


    app = QApplication([])

    LOG.debug(f"Adding Roboto font to application from {assets.get_roboto_font()}")
    QFontDatabase.addApplicationFont(assets.get_roboto_font())
    QApplication.setFont(QFont("Roboto-Regular", 12))

    app.setApplicationName("Avamp")
    app.setStyleSheet(styles.dark())

    main_window = MainWindow(roolt_path=root_path)
    main_window.setWindowFlags(main_window.windowFlags() | Qt.WindowType.MSWindowsOwnDC | Qt.WindowType.NoTitleBarBackgroundHint | Qt.WindowType.ExpandedClientAreaHint)
    main_window.show()
    app.exec()