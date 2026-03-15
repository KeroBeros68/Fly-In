class Link():
    """
    Representation of a graph link between two hubs.

    Attributes:
        name (str): The name or identifier of the link.
        max_drones (int): The current structural limit for number of drones.
    """

    def __init__(self, name: str, max_drones: int) -> None:
        """
        Initializes a link.

        Args:
            name (str): Link identifier (e.g. 'A-B').
            max_drones (int): Maximum drone capacity on the link.
        """
        self.__name: str = name
        self.__max_drones: int = max_drones

    @property
    def name(self) -> str:
        """
        Gets the name of the link.

        Returns:
            str: The name.
        """
        return self.__name

    @property
    def max_drone(self) -> int:
        """
        Gets the drone capacity of the link.

        Returns:
            int: Ensure drone limit parameter value.
        """
        return self.__max_drones
