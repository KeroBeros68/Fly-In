import math

from typing import List, Optional, Tuple


class Node:
    def __init__(
        self,
        name: str,
        type: str,
        pos: Tuple[int, int],
        zone: str,
        color: Optional[str] = None,
    ) -> None:
        self.__name: str = name
        self.__type: str = type
        self.__pos: Tuple[int, int] = pos

        self.__weight: float = math.inf
        self.__connected_node: List[Node] = []

        self.__color: Optional[str] = color
        self.__zone: str = zone

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> str:
        return self.__type

    @property
    def pos(self) -> Tuple[int, int]:
        return self.__pos

    @property
    def color(self) -> str | None:
        return self.__color

    @property
    def zone(self) -> str:
        return self.__zone

    @property
    def weight(self) -> float:
        return self.__weight

    @weight.setter
    def weight(self, new_weight: float) -> None:
        self.__weight = new_weight

    @property
    def connected_nodes(self) -> List["Node"]:
        return self.__connected_node

    def add_connected_node(self, new_node: "Node") -> None:
        if new_node in self.__connected_node or new_node.name == self.name:
            raise NodeConnectedNodeError(
                f"new_node {new_node.name} for {self.__name}"
            )
        self.__connected_node.append(new_node)


class NodeError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"[NodeError] {self.message}"


class NodeConnectedNodeError(NodeError):
    def __init__(self, message: str):
        super().__init__(message)
