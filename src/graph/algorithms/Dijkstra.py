import heapq
import logging
import math

from src.graph.Graph import Graph
from src.graph.node import Node

logger = logging.getLogger("Fly-In")


class Djikstra:
    @staticmethod
    def dijkstra(graph: Graph):

        distances = {node: float("inf") for node in graph.nodes.keys()}
        previous = {}

        start: Node = graph.nodes["start"]
        end: Node = (
            graph.nodes["goal"]
            if graph.nodes.get("goal")
            else graph.nodes["impossible_goal"]
        )
        distances[start.name] = 0

        queue: list[tuple[float, int, str]] = [(0.0, 0, start.name)]

        while queue:
            current_dist, current_round, current_node = heapq.heappop(queue)
            if current_node == end.name:
                break

            for neighbor in graph.nodes[current_node].connected_nodes:
                distance = current_dist + (
                    1
                    if neighbor.zone == "normal"
                    else (
                        0.9
                        if neighbor.zone == "priority"
                        else 2 if neighbor.zone == "restricted" else math.inf
                    )
                )

                if distance < distances[neighbor.name]:
                    distances[neighbor.name] = distance
                    previous[neighbor.name] = current_node
                    heapq.heappush(
                        queue, (distance, current_round, neighbor.name)
                    )
                current_round += 1

        path = []
        node = end.name

        while node != start.name:
            path.append((node, current_round))
            node = previous[node]
            current_round -= 1

        path.append((start.name, current_round))
        path.reverse()

        return path, distances[end.name]
