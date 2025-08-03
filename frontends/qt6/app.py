from PyQt6.QtWidgets import QApplication
from frontends.qt6.widgets.mainwindow import MainWindow


def main():
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()