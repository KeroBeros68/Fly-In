from typing import Protocol, runtime_checkable

from src.graph.Graph import Graph


@runtime_checkable
class AlgorithmProtocol(Protocol):
    def process(
        self,
        graph: Graph,
        occupancy: dict[int, dict[str, int]],
        link_occupancy: dict[int, dict[str, int]]
    ) -> dict[int, str]: ...
