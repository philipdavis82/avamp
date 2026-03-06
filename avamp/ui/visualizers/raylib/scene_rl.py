from avamp.core.logging import LOG
from avamp.core.dispatcher import VisualDispatcher
import raylib as rl

from avamp.core.interfaces.scene_3d_interface import Scene3DInterface


class SceneRLVisualizer:
    """
    Visualizer for 3D scenes using raylib.
    """
    _interface: Scene3DInterface
    _window_width: int
    _window_height: int
    _window_title: str

    def __init__(self, interface: Scene3DInterface, window_width=800, window_height=600, window_title="3D Scene"):
        """
        Initialize the 3D scene visualizer.

        :param interface: The Scene3DInterface to visualize.
        :param window_width: Width of the window.
        :param window_height: Height of the window.
        :param window_title: Title of the window.
        """
        self._interface = interface
        self._window_width = window_width
        self._window_height = window_height
        self._window_title = window_title

        # Initialize raylib
        rl.init_window(self._window_width, self._window_height, self._window_title)
        rl.set_target_fps(60)
        self.render()

    def render(self):
        """
        Render the 3D scene.
        """
        while not rl.window_should_close():
            rl.begin_drawing()
            rl.clear_background(rl.RAYWHITE)

            rl.begin_mode3d(rl.Camera(
                position=rl.Vector3(0.0, 10.0, 10.0),
                target=rl.Vector3(0.0, 0.0, 0.0),
                up=rl.Vector3(0.0, 1.0, 0.0),
                fovy=45.0,
                type=rl.CAMERA_PERSPECTIVE
            ))

            for obj in self._interface.objects:
                if obj['type'] == 'cube':
                    rl.draw_cube(rl.Vector3(*obj['position']), *obj['size'], rl.Color(int(obj['color'][0]*255), int(obj['color'][1]*255), int(obj['color'][2]*255), 255))
                elif obj['type'] == 'sphere':
                    rl.draw_sphere(rl.Vector3(*obj['position']), obj['radius'], rl.Color(int(obj['color'][0]*255), int(obj['color'][1]*255), int(obj['color'][2]*255), 255))
                # Add more object types as needed

            rl.end_mode3d()
            rl.draw_text("3D Scene Visualization", 10, 10, 20, rl.DARKGRAY)
            rl.end_drawing()
    
    def show(self):
        """
        Show the visualizer window.
        """
        rl.window_should_close()
VisualDispatcher.add_visual(SceneRLVisualizer, "line")