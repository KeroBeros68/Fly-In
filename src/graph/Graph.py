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

    @property
    def nodes(self) -> list[Node]:
        return self.__nodes

    @property
    def links(self) -> Dict[str, Link]:
        return self.__links

    def add_node(self, node: Node) -> None:
        if node in self.__nodes:
            raise GraphNodeError("Node already in Graph")
        self.__nodes.append(node)

    def add_link(self, link: Link) -> None:
        if link.name in self.__links:
            raise GraphLinkError("Link already in Graph")
        self.__links[link.name] = link


class GraphError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Graph error: {message}")


class GraphNodeError(GraphError):
    def __init__(self, message: str):
        super().__init__(message)


class GraphLinkError(GraphError):
    def __init__(self, message: str):
        super().__init__(message)
