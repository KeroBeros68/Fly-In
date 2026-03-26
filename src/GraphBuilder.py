import logging

from src.graph.Graph import Graph
from src.graph.link import Link
from src.graph.node import Node
from src.graph.node.EndNode import EndNode
from src.graph.node.HubNode import HubNode
from src.graph.node.StartNode import StartNode
from src.parsing.models.MapModel import MapModel


class GraphBuilder:
    """
    Builds a Graph instance from a parsed MapModel.

    Converts the abstract model data (hubs, connections) into
    concrete Node and Link objects within a Graph.
    """

    def __init__(self) -> None:
        """Initializes the GraphBuilder with a logger."""
        self.logger = logging.getLogger("Fly-In")

    def build(self, map_model: MapModel, map_name: str) -> Graph:
        """
        Constructs and returns a Graph from the given map model.

        Args:
            map_model (MapModel): The parsed map data containing hubs and
            connections.
            map_name (str): The name to assign to the resulting graph.

        Returns:
            Graph: A fully connected graph with nodes and links.
        """
        graph = Graph()
        graph.name = map_name
        hubs = map_model.hubs.copy()

        end_node = EndNode(
            map_model.end_hub.name,
            map_model.end_hub.pos,
            map_model.end_hub.zone.value,
            map_model.end_hub.color,
            map_model.end_hub.max_drones
        )
        graph.add_node(end_node)

        start_node = StartNode(
            map_model.start_hub.name,
            map_model.start_hub.pos,
            map_model.start_hub.zone.value,
            map_model.start_hub.color,
            map_model.start_hub.max_drones
        )
        graph.add_node(start_node)

        for hub in hubs:
            node: Node = HubNode(
                hub.name,
                hub.pos,
                hub.zone.value,
                hub.color,
                hub.max_drones
            )
            graph.add_node(node)

        for connection in map_model.connections:
            link: Link = Link(
                f"{connection.zone1}-{connection.zone2}",
                connection.max_link_capacity,
            )
            graph.nodes[connection.zone1].add_connected_node(
                graph.nodes[connection.zone2]
            )
            graph.nodes[connection.zone2].add_connected_node(
                graph.nodes[connection.zone1]
            )
            graph.add_link(link)
        self.logger.info(repr(graph))
        return graph
