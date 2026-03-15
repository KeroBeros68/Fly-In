import math

from typing import List, Optional, Tuple


class Node:
    """
    Representation of a graph Node structure mapping positions or states.

    Attributes:
        name (str): Label identity.
        type (str): Type identifier class.
        pos (Tuple[int, int]): Cartesian (x,y) location.
        zone (str): Sub-division logic grouping.
        color (Optional[str]): Render attribute formatting.
        weight (float): Weighted capacity metric default of infinity.
    """

    def __init__(
        self,
        name: str,
        type: str,
        pos: Tuple[int, int],
        zone: str,
        color: Optional[str] = None,
    ) -> None:
        """
        Initializes graph components for the Node.

        Args:
            name (str): Nominal label string.
            type (str): Sub logic category identifier.
            pos (Tuple[int, int]): Fixed location setup mapping.
            zone (str): Contextual zone categorization.
            color (Optional[str], optional): Cosmetic wrapper.
        """
        self.__name: str = name
        self.__type: str = type
        self.__pos: Tuple[int, int] = pos

        self.__weight: float = math.inf
        self.__connected_node: List[Node] = []

        self.__color: Optional[str] = color
        self.__zone: str = zone

    @property
    def name(self) -> str:
        """
        Gets the name identifier.

        Returns:
            str: Identity name mapping label.
        """
        return self.__name

    @property
    def type(self) -> str:
        """
        Gets node context logic type.

        Returns:
            str: Identifier sub typing context logic.
        """
        return self.__type

    @property
    def pos(self) -> Tuple[int, int]:
        """
        Retrieves positional tuple bounds.

        Returns:
            Tuple[int, int]: Value logic parameter bindings.
        """
        return self.__pos

    @property
    def color(self) -> str | None:
        """
        Accesses rendered color parameter bounds.

        Returns:
            str | None: The formatted layout configuration wrapper.
        """
        return self.__color

    @property
    def zone(self) -> str:
        """
        Accessor context for group assignments parameters.

        Returns:
            str: Sub-division logic grouping.
        """
        return self.__zone

    @property
    def weight(self) -> float:
        """
        Access default internal node's weight.

        Returns:
            float: The current weight of the node.
        """
        return self.__weight

    @weight.setter
    def weight(self, new_weight: float) -> None:
        """
        Modifies node traversal parameter value weight.

        Args:
            new_weight (float): The new weight value to assign.
        """
        self.__weight = new_weight

    @property
    def connected_nodes(self) -> List["Node"]:
        """
        Retrieves the list of connected nodes.

        Returns:
            List[Node]: Connected node instances.
        """
        return self.__connected_node

    def add_connected_node(self, new_node: "Node") -> None:
        """
        Appends a uniquely newly connected node into the adjacency list.

        Args:
            new_node (Node): Node reference to connect.

        Raises:
            NodeConnectedNodeError: Occurs if the target already exists.
        """
        if new_node in self.__connected_node or new_node.name == self.name:
            raise NodeConnectedNodeError(
                f"new_node {new_node.name} for {self.__name}"
            )
        self.__connected_node.append(new_node)


class NodeError(Exception):
    """
    Base exception for node-related problems.
    """

    def __init__(self, message: str):
        """
        Initializes limit states exception overrides collections bounds.

        Args:
            message (str): Information associated with this failure state.
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """
        Formats exception details structure values mapping references.

        Returns:
            str: Formatted error outputs context variables definitions.
        """
        return f"[NodeError] {self.message}"


class NodeConnectedNodeError(NodeError):
    """
    Subclass error covering exceptions triggered with adjacency modifications.
    """

    def __init__(self, message: str):
        """
        Initializes graph linking limits states.

        Args:
            message (str): Description string highlighting the conflict.
        """
        super().__init__(message)
