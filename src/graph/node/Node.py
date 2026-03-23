import math

from typing import Optional


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
        pos: tuple[int, int],
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
        self.__pos: tuple[int, int] = pos

        self.__weight: float = math.inf
        self.__connected_node: list[Node] = [self]
        self.__previous_node: str = ""

        self.__max_drones: int = 1
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
    def pos(self) -> tuple[int, int]:
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
    def max_drones(self) -> int:
        return self.__max_drones

    @max_drones.setter
    def max_drones(self, max_drones: int) -> None:
        self.__max_drones = max_drones

    @property
    def connected_nodes(self) -> list["Node"]:
        """
        Retrieves the list of connected nodes.

        Returns:
            List[Node]: Connected node instances.
        """
        return self.__connected_node

    @property
    def previous_node(self) -> str:
        return self.__previous_node

    @previous_node.setter
    def previous_node(self, node: "Node") -> None:
        self.__previous_node = node.name

    def add_connected_node(self, new_node: "Node") -> None:
        """
        Appends a uniquely newly connected node into the adjacency list.

        Args:
            new_node (Node): Node reference to connect.

        Raises:
            NodeConnectedNodeError: Occurs if the target already exists.
        """
        if new_node in self.__connected_node:
            raise NodeConnectedNodeError(
                f"new_node {new_node.name} for {self.__name}"
            )
        self.__connected_node.append(new_node)

    def __repr__(self) -> str:
        res: str = (
            f"{self.__name} {self.__pos} {self.__weight}"
            f" {self.__color} {self.__zone}"
        )
        for node in self.connected_nodes:
            res += f"\n{node.name}"
        return res

    def __lt__(self, other: "Node") -> bool:
        return self.name < other.name


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
