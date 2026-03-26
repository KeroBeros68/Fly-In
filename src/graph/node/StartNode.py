from typing import Optional

from src.graph.node.Node import Node


class StartNode(Node):
    """The starting node in the simulation graph where all drones begin."""

    def __init__(
        self,
        name: str,
        pos: tuple[int, int],
        zone: str,
        color: Optional[str] = None,
        max_drone: int = 1
    ) -> None:
        """
        Initializes the StartNode.

        Args:
            name (str): Unique name identifier for the node.
            pos (Tuple[int, int]): Cartesian (x, y) position on the map.
            zone (str): Zone category this node belongs to.
            color (Optional[str], optional): Optional rendering color.
            max_drone (int, optional): Maximum simultaneous drones. Defaults
            to 1.
        """
        super().__init__(name, pos, zone, color, max_drone)
