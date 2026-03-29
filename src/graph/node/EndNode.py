from typing import Optional

from src.graph.node.Node import Node


class EndNode(Node):
    """
    The destination node in the simulation graph where drones must arrive.
    """

    def __init__(
        self,
        name: str,
        pos: tuple[int, int],
        zone: str,
        color: Optional[str] = None,
        max_drone: int = 1
    ) -> None:
        """
        Initializes the EndNode.

        Args:
            name (str): Unique name identifier for the node.
            pos (Tuple[int, int]): Cartesian (x, y) position on the map.
            zone (str): Zone category this node belongs to.
            color (Optional[str], optional): Optional rendering color.
            max_drone (int, optional): Maximum simultaneous drones. Defaults
            to 1.
        """
        super().__init__(name, pos, zone, color, max_drone)

    @property
    def is_terminal(self) -> bool:
        """
        Returns True because the end node is exempt from capacity limits.

        Multiple drones can arrive and accumulate at the end node
        regardless of its max_drones setting.

        Returns:
            bool: Always True.
        """
        return True
