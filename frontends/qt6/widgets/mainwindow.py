from PyQt6.QtWidgets import QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VAMP Main Window")
        self.resize(800, 600)

    def show(self):
        super().show()
        print("Main window is now visible.")