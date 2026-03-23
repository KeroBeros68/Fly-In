import logging

from src.graph.Graph import Graph
from src.graph.link import Link
from src.graph.node import Node
from src.graph.node.EndNode import EndNode
from src.graph.node.HubNode import HubNode
from src.graph.node.StartNode import StartNode
from src.parsing.models.MapModel import MapModel


class GraphBuilder:
    def __init__(self) -> None:
        self.logger = logging.getLogger("Fly-In")

    def build(self, map_model: MapModel, map_name: str) -> Graph:
        graph = Graph()
        graph.name = map_name
        hubs = map_model.hubs.copy()

        end_node = EndNode(
            map_model.end_hub.name,
            map_model.end_hub.pos,
            map_model.end_hub.zone.value,
            map_model.end_hub.color,
        )
        graph.add_node(end_node)

        start_node = StartNode(
            map_model.start_hub.name,
            map_model.start_hub.pos,
            map_model.start_hub.zone.value,
            map_model.start_hub.color,
        )
        graph.add_node(start_node)

        for hub in hubs:
            node: Node = HubNode(
                hub.name,
                hub.pos,
                hub.zone.value,
                hub.color,
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
