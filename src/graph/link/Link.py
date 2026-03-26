from typing import Optional


class Link:
    """
    Represents a directional link (corridor) between two nodes in the graph.

    Attributes:
        name (str): Identifier of the link, typically 'NodeA-NodeB'.
        max_drone (int | None): Maximum number of drones allowed on this link
        simultaneously.
    """

    def __init__(self, name: str, max_links: Optional[int] = 1) -> None:
        """
        Initializes a Link between two nodes.

        Args:
            name (str): Link identifier (e.g. 'A-B').
            max_links (Optional[int]): Maximum simultaneous drone capacity on
            the link.
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
        Gets the maximum number of drones allowed on this link simultaneously.

        Returns:
            int | None: The drone capacity, or None if unlimited.
        """
        return self.__max_links
