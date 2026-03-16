from typing import Optional


class Link():
    """
    Representation of a graph link between two hubs.

    Attributes:
        name (str): The name or identifier of the link.
        max_links (int): The current structural limit for number of links.
    """

    def __init__(self, name: str, max_links: Optional[int]) -> None:
        """
        Initializes a link.

        Args:
            name (str): Link identifier (e.g. 'A-B').
            max_links (int): Maximum drone capacity on the link.
        """
        self.__name: str = name
        self.__max_links: Optional[int] = max_links

    @property
    def name(self) -> str:
        """
        Gets the name of the link.

        Returns:
            str: The name.
        """
        return self.__name

    @property
    def max_drone(self) -> int | None:
        """
        Gets the drone capacity of the link.

        Returns:
            int: Ensure drone limit parameter value.
        """
        return self.__max_links
