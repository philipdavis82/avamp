# Global Imports
from avamp.core.logging import LOG
from avamp.core.dispatcher import VisualDispatcher

# Type Imports
from avamp.ui.visualizers.QtGL.opengl_scene   import GLScene
from avamp.ui.visualizers.QtGL.opengl_context import GlWidget
from avamp.core.interfaces.scene_3d_interface import Scene3DInterface

# Library Imports
from PySide6.QtWidgets import QWidget, QGridLayout, QMenuBar, QMenu, QApplication, QStatusBar, QSizePolicy, QSlider, QPushButton
from PySide6.QtCore import Qt

class PlayPauseButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setText("Play")
        self.toggled.connect(self.toggle_play_pause)

    def toggle_play_pause(self, checked):
        if checked:
            self.setText("Pause")
            # Start playing the animation
        else:
            self.setText("Play")
            # Pause the animation

class SimpleOglVisualizer (QWidget):
    def __init__(self, data=None, filename=None, parent=None):
        super().__init__(parent)

        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._glWidget = GlWidget(self)
        self._layout.addWidget(self._glWidget, 0, 0, 1, 2)

        self._playPauseButton = PlayPauseButton(self)
        self._timeSlider = QSlider(self)
        self._timeSlider.setOrientation(Qt.Orientation.Horizontal)
        self._timeSlider.setRange(0, 100)
        self._timeSlider.setValue(0)

        self._layout.addWidget(self._playPauseButton, 1, 0)
        self._layout.addWidget(self._timeSlider, 1, 1)

        LOG.debug(f"Initialized SimpleOglVisualizer with data: {data} and filename: {filename}")

        self.scene = GLScene()
        if data:
            self.parseData(data)

    def parseData(self, data):
        """
        Parse the provided data and update the visualizer accordingly.

        :param data: The data to be parsed, expected to be a Scene3DInterface instance.
        """
        if isinstance(data, Scene3DInterface):
            LOG.debug("Parsing Scene3DInterface data for SimpleOglVisualizer.")
            self.parseScene3DInterface(data)
        else:
            LOG.error("Unsupported data type for SimpleOglVisualizer. Expected Scene3DInterface.")

    def parseScene3DInterface(self, scene: Scene3DInterface):
        """
        Parse the provided Scene3DInterface data and update the visualizer accordingly.

        :param scene: The Scene3DInterface instance to be parsed.
        """
        LOG.debug("Parsing Scene3DInterface data for SimpleOglVisualizer.")
        
        
        


VisualDispatcher.add_visual(SimpleOglVisualizer, "3d_scene")


