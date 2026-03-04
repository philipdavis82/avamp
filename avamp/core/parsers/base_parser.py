class InterfaceGroup:
    """
    This Groups interfaces together for the UI.
    """
    def __init__(self, name: str, data: dict[any]):
        """
        Initialize the interface group.

        :param name: The name of the interface group.
        :param keys: The keys associated with the interface group.
        :param data: The data associated with the interface group.
        """
        self._name = name
        self._data = data
    def name(self) -> str:
        """Return the name of the interface group."""
        return self._name
    def data(self) -> dict[any]:
        """Return the data associated with the interface group."""
        return self._data
    def __iter__(self):
        """Iterate over the data items in the interface group."""
        return iter(self._data.items())

class BaseParser:
    """
    Base class for parsers.
    """
    def __init__(self, file_path: str = None):
        """
        Initialize the base parser.

        :param file_path: Optional path to a file to be parsed.
        """
        # raise NotImplementedError("Subclasses must implement this method.")

    def name(self) -> str:
        """
        Return the name of the parser.

        :return: The name of the parser.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def keys(self) -> list[str]:
        """
        Return the keys of the parser.

        :return: A list of keys.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    def data(self, *args, **kwargs) -> any:
        """
        Return the data associated with the parser.

        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The data associated with the parser.
        """
        raise NotImplementedError("Subclasses must implement this method.")