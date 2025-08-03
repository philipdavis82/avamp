class BaseInterface:
    """
    Base interface for all interfaces in the application.
    This class should be inherited by all interface classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the base interface.
        """
        pass

    def type(self) -> str:
        """
        Return the type of the interface.
        This method should be implemented by subclasses to return a specific type.
        
        :return: A string representing the type of the interface.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def data(self,*args,**kwargs) -> any :
        """
        Return the data associated with the interface.
        This method should be implemented by subclasses to return specific data.
        
        :return: The data associated with the interface.
        """
        raise NotImplementedError("Subclasses must implement this method.")