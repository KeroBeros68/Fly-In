from typing import Optional

from src.graph.node.Node import Node


class EndNode(Node):
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
        super().__init__(name, pos, zone, color)
