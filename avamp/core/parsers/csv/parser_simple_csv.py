from avamp.core.logging import LOG
from avamp.core.parsers.base_parser import BaseParser
from avamp.core.interfaces.lines.simple_line_interface import SimpleLineInterface

class SimpleCsvParser (BaseParser):
    """
    A simple CSV parser that extends the BaseParser class.
    This parser is designed to handle basic CSV parsing functionality.

    Assumes time is the frirst column
    """

    def __init__(self, file_path: str):
        """
        Initialize the SimpleCsvParser with an optional file path.

        :param file_path: Optional path to a CSV file to be parsed.
        """
        super().__init__(file_path)
        self.file_path = file_path
        self._headers = []
        self._raw_data = {}
        self._data = {}

        self._parse_csv()  # Parse the CSV file
        self._create_interfaces()
        # Parsing CSV file
    
    def keys(self) -> list[str]:
        """
        Return the keys of the parser, which are the headers of the CSV file.

        :return: A list of headers from the CSV file.
        """
        return self._headers
    
    def data(self, key) -> any:
        """
        Return the data associated with the parser, which is a dictionary of SimpleLineInterface instances.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: A dictionary where keys are headers and values are SimpleLineInterface instances.
        """
        return self._data[key]
    
    def _parse_csv(self):
        """
        Parse the CSV file and populate the data attribute.
        This method should be implemented to read the CSV file and extract data.
        """
        import csv
        with open(self.file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for key, value in row.items():
                    if key not in self._headers:
                        self._headers.append(key)
                    if key not in self._raw_data:
                        self._raw_data[key] = []
                    self._raw_data[key].append(float(value))
    
    def _create_interfaces(self):
        """
        Create interfaces from the parsed data.
        This method converts the parsed data into SimpleLineInterface instances.
        """
        LOG.debug("Creating interfaces from parsed data")
        time = self._raw_data[self._headers[0]]
        LOG.debug(f"Time data: {self._headers[0]}")
        for key in self._headers:
            self._data[key] = SimpleLineInterface(
                x=time,
                y=self._raw_data[key],
                x_name=self._headers[0],
                y_name=key
            )
            LOG.debug(f"Found Data: {key}")

    


PARSER_EXT  = [    "csv",]
PARSER_CLS  = SimpleCsvParser
PARSER_NAME = SimpleCsvParser.__name__