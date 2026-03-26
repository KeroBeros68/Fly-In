from typing import Protocol, runtime_checkable

from src.graph.Graph import Graph


@runtime_checkable
class AlgorithmProtocol(Protocol):
    """
    Protocol defining the interface that all pathfinding algorithms must
    implement.

    Any class implementing this protocol can be used as a drop-in algorithm
    for the simulation engine.
    """

    def process(
        self,
        graph: Graph,
        occupancy: dict[int, dict[str, int]],
        link_occupancy: dict[int, dict[str, int]],
    ) -> dict[int, str]:
        """
        Computes the path for a single drone through the graph.

        Args:
            graph (Graph): The graph to traverse.
            occupancy (dict[int, dict[str, int]]): Node occupancy counts per
            turn.
            link_occupancy (dict[int, dict[str, int]]): Link occupancy counts
            per turn.

        Returns:
            dict[int, str]: Mapping of turn number to node name for the
            drone's path.
        """
        ...
