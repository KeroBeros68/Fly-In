import math

from typing import Optional


from abc import ABC, abstractmethod


class INode(ABC):
    """Identité de base d'un noeud."""

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Gets the unique name identifier of the node.

        Returns:
            str: The node's name.
        """
        ...

    @property
    @abstractmethod
    def pos(self) -> tuple[int, int]:
        """
        Gets the (x, y) position of the node on the map.

        Returns:
            tuple[int, int]: Cartesian position of the node.
        """
        ...

    @property
    @abstractmethod
    def zone(self) -> str:
        """
        Gets the zone category this node belongs to.

        Returns:
            str: The zone name (e.g., 'normal', 'priority', 'restricted').
        """
        ...

    @property
    @abstractmethod
    def is_terminal(self) -> bool:
        """
        Whether this node is a terminal (start or end) node.

        Terminal nodes are exempt from capacity constraints so that
        all drones can depart from start and accumulate at end freely.

        Returns:
            bool: True if this node is a start or end node.
        """
        ...


class IPathfindingNode(INode):
    """Noeud capable de participer à un algorithme de pathfinding."""

    @property
    @abstractmethod
    def weight(self) -> float:
        """
        Gets the pathfinding weight of the node.

        Returns:
            float: The current weight (infinity by default).
        """
        ...

    @weight.setter
    @abstractmethod
    def weight(self, value: float) -> None:
        """
        Sets the pathfinding weight of the node.

        Args:
            value (float): The new weight value to assign.
        """
        ...

    @property
    @abstractmethod
    def previous_node(self) -> str:
        """
        Gets the name of the previous node in the pathfinding traversal.

        Returns:
            str: The name of the predecessor node, or empty string if none.
        """
        ...

    @property
    @abstractmethod
    def connected_nodes(self) -> list["IPathfindingNode"]:
        """
        Gets the list of directly connected neighbour nodes.

        Returns:
            list[IPathfindingNode]: Connected node instances.
        """
        ...

    @abstractmethod
    def add_connected_node(self, node: "IPathfindingNode") -> None:
        """
        Adds a node to the adjacency list.

        Args:
            node (IPathfindingNode): The neighbour node to connect.
        """
        ...


class IDroneNode(INode):
    """Noeud avec capacité de gestion de drones."""

    @property
    @abstractmethod
    def max_drones(self) -> int:
        """
        Gets the maximum number of drones allowed on this node simultaneously.

        Returns:
            int: The drone capacity of the node.
        """
        ...

    @max_drones.setter
    @abstractmethod
    def max_drones(self, value: int) -> None:
        """
        Sets the maximum number of drones allowed on this node.

        Args:
            value (int): The new drone capacity.
        """
        ...


class Node(IDroneNode, IPathfindingNode):
    """
    Representation of a graph node with position, zone, and capacity.

    Attributes:
        name (str): Unique label identifying the node.
        pos (Tuple[int, int]): Cartesian (x, y) position on the map.
        zone (str): Zone category the node belongs to.
        color (Optional[str]): Optional color used for rendering.
        weight (float): Pathfinding weight, defaults to infinity.
        max_drones (int): Maximum number of drones allowed on this node
        simultaneously.
    """

    def __init__(
        self,
        name: str,
        pos: tuple[int, int],
        zone: str,
        color: Optional[str] = None,
        max_drone: int = 1,
    ) -> None:
        """
        Initializes a Node with its identity, position, and optional
        attributes.

        Args:
            name (str): Unique name identifier for the node.
            pos (Tuple[int, int]): Cartesian (x, y) position on the map.
            zone (str): Zone category this node belongs to.
            color (Optional[str], optional): Optional rendering color.
            max_drone (int, optional): Maximum simultaneous drones. Defaults
            to 1.
        """
        self.__name: str = name
        self.__pos: tuple[int, int] = pos

        self.__weight: float = math.inf
        self.__connected_node: list[IPathfindingNode] = [self]
        self.__previous_node: str = ""

        self.__max_drones: int = max_drone
        self.__color: Optional[str] = color
        self.__zone: str = zone

    @property
    def is_terminal(self) -> bool:
        """
        Returns False for all regular nodes.

        Overridden to True in StartNode and EndNode, which are exempt
        from drone capacity limits.

        Returns:
            bool: Always False for intermediate hub nodes.
        """
        return False

    @property
    def name(self) -> str:
        """
        Gets the unique name identifier of the node.

        Returns:
            str: The node's name.
        """
        return self.__name

    @property
    def pos(self) -> tuple[int, int]:
        """
        Gets the (x, y) position of the node on the map.

        Returns:
            Tuple[int, int]: Cartesian position of the node.
        """
        return self.__pos

    @property
    def color(self) -> str | None:
        """
        Gets the optional rendering color of the node.

        Returns:
            str | None: The color string, or None if not set.
        """
        return self.__color

    @property
    def zone(self) -> str:
        """
        Gets the zone category this node belongs to.

        Returns:
            str: The zone name (e.g., 'normal', 'priority', 'restricted').
        """
        return self.__zone

    @property
    def weight(self) -> float:
        """
        Gets the pathfinding weight of the node.

        Returns:
            float: The current weight (infinity by default).
        """
        return self.__weight

    @weight.setter
    def weight(self, new_weight: float) -> None:
        """
        Sets the pathfinding weight of the node.

        Args:
            new_weight (float): The new weight value to assign.
        """
        self.__weight = new_weight

    @property
    def max_drones(self) -> int:
        """
        Gets the maximum number of drones allowed on this node simultaneously.

        Returns:
            int: The drone capacity of the node.
        """
        return self.__max_drones

    @max_drones.setter
    def max_drones(self, max_drones: int) -> None:
        """
        Sets the maximum number of drones allowed on this node.

        Args:
            max_drones (int): The new drone capacity.
        """
        self.__max_drones = max_drones

    @property
    def connected_nodes(self) -> list["IPathfindingNode"]:
        """
        Retrieves the list of connected nodes.

        Returns:
            list[IPathfindingNode]: Connected node instances.
        """
        return self.__connected_node

    @property
    def previous_node(self) -> str:
        """
        Gets the name of the previous node in the pathfinding traversal.

        Returns:
            str: The name of the predecessor node, or empty string if none.
        """
        return self.__previous_node

    @previous_node.setter
    def previous_node(self, node: "Node") -> None:
        """
        Records the name of the predecessor node during pathfinding.

        Args:
            node (Node): The predecessor node to store.
        """
        self.__previous_node = node.name

    def add_connected_node(self, new_node: "IPathfindingNode") -> None:
        """
        Appends a uniquely newly connected node into the adjacency list.

        Args:
            new_node (IPathfindingNode): Node reference to connect.

        Raises:
            NodeConnectedNodeError: Occurs if the target already exists.
        """
        if new_node in self.__connected_node:
            raise NodeConnectedNodeError(
                f"new_node {new_node.name} for {self.__name}"
            )
        self.__connected_node.append(new_node)

    def __repr__(self) -> str:
        """
        Returns a string representation of the node including position,
        weight, color, zone, and connected node names.

        Returns:
            str: Human-readable description of the node.
        """
        res: str = (
            f"{self.__name} {self.__pos} {self.__weight}"
            f" {self.__color} {self.__zone}"
        )
        for node in self.connected_nodes:
            res += f"\n{node.name}"
        return res

    def __lt__(self, other: "Node") -> bool:
        """
        Compares nodes by name for ordering (used in priority queues).

        Args:
            other (Node): The other node to compare with.

        Returns:
            bool: True if this node's name is lexicographically less than
            other's.
        """
        return self.name < other.name


class NodeError(Exception):
    """
    Base exception for node-related errors.
    """

    def __init__(self, message: str):
        """
        Initializes the NodeError with a descriptive message.

        Args:
            message (str): Description of the node error.
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the error.

        Returns:
            str: Error message prefixed with [NodeError].
        """
        return f"[NodeError] {self.message}"


class NodeConnectedNodeError(NodeError):
    """
    Raised when attempting to add a node that is already in the adjacency list.
    """

    def __init__(self, message: str):
        """
        Initializes the NodeConnectedNodeError with a conflict description.

        Args:
            message (str): Description of the duplicate connection conflict.
        """
        super().__init__(message)
