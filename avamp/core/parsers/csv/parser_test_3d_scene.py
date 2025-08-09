from avamp.core.logging import LOG
from avamp.core.parsers.base_parser import BaseParser
from avamp.core.interfaces.scene_3d_interface import Scene3DInterface

"""
"objects": [
        {
            "name": "Cube1",
            "type": "cube",
            "position": [0,0,0],
            "size": [1,1,1],
            "color": [1,0,0],
            "rotation": [
                [1,0,0],
                [0,1,0],
                [0,0,1]
            ],
            "scale": [1,1,1],
            "visible": true,
            "shape": "cube"
        },
"""

class Test3DScene (BaseParser):
    """
    This parses a json file containing a 3D scene.
    """

    def __init__(self, file_path: str):
        """
        Initialize the Test3DScene parser with an optional file path.

        :param file_path: Optional path to a JSON file to be parsed.
        """
        super().__init__(file_path)
        self.file_path = file_path
        self._raw_data = {}
        self._data = {}

        self._parse_json()  # Parse the JSON file
        self._create_interfaces()
    
    def _parse_json(self):
        """
        Parse the JSON file and populate the data attribute.
        This method should be implemented to read the JSON file and extract data.
        """
        import json
        with open(self.file_path, 'r') as jsonfile:
            self._raw_data = json.load(jsonfile)
        
    def _create_interfaces(self):
        """
        Create interfaces from the parsed JSON data.
        This method should be implemented to convert the raw data into interfaces.
        """
        objects = self._raw_data.get('objects', [])
        scene = Scene3DInterface()
        for obj in objects:
            name = obj.get('name', 'Unnamed')
            position = obj.get('position', [0, 0, 0])
            rotation = obj.get('rotation', [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            scale = obj.get('scale', [1, 1, 1])
            new_obj = Scene3DInterface.Object3D(
                name=name,
                position=position,
                rotation=rotation,
                scale=scale
            )
            if(obj.get('shape')):
                new_obj.set_shape(obj['shape'])
        self._data['scene'] = scene
    
    

        


    def name(self) -> str:
        """
        Return the name of the parser.

        :return: The name of the parser.
        """
        return self.__class__.__name__
    
    def keys(self) -> list[str]:
        """
        Return the keys of the parser, which are the headers of the JSON file.

        :return: A list of headers from the JSON file.
        """
        return list(self._raw_data.keys())

    def data(self, key) -> any:
        """
        Return the data associated with the parser, which is a dictionary of Scene3DInterface instances.
        
        :param key: The key to retrieve data for.
        :return: A dictionary where keys are headers and values are Scene3DInterface instances.
        """
        return self._data.get(key, None)
    
    def __iter__(self):
        """
        Make the parser iterable, allowing iteration over the keys of the data.
        
        :return: An iterator over the keys of the data.
        """
        return iter(self._data.keys())
    

    
PARSER_EXT  = [    ".json3d",]
PARSER_CLS  = Test3DScene
PARSER_NAME = Test3DScene.__name__