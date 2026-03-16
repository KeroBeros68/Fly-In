from typing import Dict, List

from src.graph.link import Link
from src.graph.node import Node


class Graph:
    """
    Represents a graph structure with nodes and links.

    Attributes:
        _nodes (List[Node]): A list of Node objects within the graph.
        _links (Dict[str, Link]): A dict mapping link names to Link objects.
    """

    def __init__(self) -> None:
        """
        Initializes an empty graph.
        """
        self.__nodes: List[Node] = []
        self.__links: Dict[str, Link] = {}
