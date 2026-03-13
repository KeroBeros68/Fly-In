import math

from typing import Optional, Tuple


class Node:
    def __init__(
        self,
        name: str,
        type: str,
        pos: Tuple[int, int],
        color: Optional[str],
        zone: str,
    ) -> None:
        self.__name: str = name
        self.__type: str = type
        self.__pos: Tuple[int, int] = pos

        self.__pond: float = math.inf
        self.__connected_node: list[Node] = []

        self.__color: Optional[str] = color
        self.__zone: str = zone
