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