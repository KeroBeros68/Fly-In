from typing import Dict, List

from src.graph.link import Link
from src.graph.node import Node


class Graph():
    def __init_(self) -> None:
        self.__nodes: List[Node] = []
        self.__links: Dict[str, Link] = {}
