from typing import Dict

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
        self.__name: str = ""
        self.__nodes: Dict[str, Node] = {}
        self.__links: Dict[str, Link] = {}

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @property
    def nodes(self) -> Dict[str, Node]:
        return self.__nodes

    @property
    def links(self) -> Dict[str, Link]:
        return self.__links

    def add_node(self, node: Node) -> None:
        if node in self.__nodes:
            raise GraphNodeError("Node already in Graph")
        if node.type == "start_hub":
            node.weight = 0
        self.__nodes[node.name] = node

    def add_link(self, link: Link) -> None:
        if link.name in self.__links:
            raise GraphLinkError("Link already in Graph")
        self.__links[link.name] = link

    def __repr__(self) -> str:
        res: str = ""
        for node in self.nodes.values():
            res += f"\n{repr(node)}\n"
        return res


class GraphError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Graph error: {message}")


class GraphNodeError(GraphError):
    def __init__(self, message: str):
        super().__init__(message)


class GraphLinkError(GraphError):
    def __init__(self, message: str):
        super().__init__(message)
