from typing import Dict

from src.graph.link import Link
from src.graph.node import Node
from src.graph.node.StartNode import StartNode


class Graph:
    """
    Represents a directed graph composed of nodes and links.

    Attributes:
        _nodes (Dict[str, Node]): A dict mapping node names to Node objects.
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
        """
        Gets the name of the graph (usually the map file name).

        Returns:
            str: The graph name.
        """
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """
        Sets the name of the graph.

        Args:
            name (str): The new name to assign.
        """
        self.__name = name

    @property
    def nodes(self) -> Dict[str, Node]:
        """
        Gets all nodes in the graph.

        Returns:
            Dict[str, Node]: Mapping of node names to Node instances.
        """
        return self.__nodes

    @property
    def links(self) -> Dict[str, Link]:
        """
        Gets all links in the graph.

        Returns:
            Dict[str, Link]: Mapping of link names to Link instances.
        """
        return self.__links

    def add_node(self, node: Node) -> None:
        """
        Adds a node to the graph.

        Args:
            node (Node): The node to add.

        Raises:
            GraphNodeError: If the node already exists in the graph.
        """
        if node in self.__nodes:
            raise GraphNodeError("Node already in Graph")
        if isinstance(node, StartNode):
            node.weight = 0
        self.__nodes[node.name] = node

    def add_link(self, link: Link) -> None:
        """
        Adds a link to the graph.

        Args:
            link (Link): The link to add.

        Raises:
            GraphLinkError: If a link with the same name already exists.
        """
        if link.name in self.__links:
            raise GraphLinkError("Link already in Graph")
        self.__links[link.name] = link

    def __repr__(self) -> str:
        """
        Returns a string representation of all nodes in the graph.

        Returns:
            str: Concatenated repr of each node.
        """
        res: str = ""
        for node in self.nodes.values():
            res += f"\n{repr(node)}\n"
        return res


class GraphError(Exception):
    """Base exception for graph-related errors."""

    def __init__(self, message: str):
        """
        Initializes the GraphError.

        Args:
            message (str): Description of the error.
        """
        super().__init__(f"Graph error: {message}")


class GraphNodeError(GraphError):
    """Raised when a node operation fails (e.g., duplicate node)."""

    def __init__(self, message: str):
        """
        Initializes the GraphNodeError.

        Args:
            message (str): Description of the node error.
        """
        super().__init__(message)


class GraphLinkError(GraphError):
    """Raised when a link operation fails (e.g., duplicate link)."""

    def __init__(self, message: str):
        """
        Initializes the GraphLinkError.

        Args:
            message (str): Description of the link error.
        """
        super().__init__(message)
