import heapq
import math

from src.graph.Graph import Graph
from src.graph.node import Node


class Dijkstra:
    @staticmethod
    def dijkstra(graph: Graph) -> list[tuple[str, int]]:

        distances = {node: float("inf") for node in graph.nodes.keys()}
        previous = {}
        node_rounds = {}

        start: Node = graph.nodes["start"]
        end: Node = (
            graph.nodes["goal"]
            if graph.nodes.get("goal")
            else graph.nodes["impossible_goal"]
        )
        distances[start.name] = 0
        node_rounds[start.name] = 0

        queue: list[tuple[float, int, str]] = [(0.0, 0, start.name)]

        while queue:
            current_dist, current_round, current_node = heapq.heappop(queue)

            node_rounds[current_node] = current_round

            if current_node == end.name:
                break

            for neighbor in graph.nodes[current_node].connected_nodes:
                distance = current_dist + (
                    1
                    if neighbor.zone == "normal"
                    else (
                        0.9999
                        if neighbor.zone == "priority"
                        else 2 if neighbor.zone == "restricted" else math.inf
                    )
                )

                arrival_round = current_round + (
                    2 if neighbor.zone == "restricted" else 1
                )
                if distance < distances[neighbor.name]:
                    distances[neighbor.name] = distance
                    previous[neighbor.name] = current_node
                    heapq.heappush(
                        queue, (distance, arrival_round, neighbor.name)
                    )

        path: list[tuple[str, int]] = []
        node_name = end.name

        while node_name != start.name:
            path.append((node_name, node_rounds[node_name]))
            if node_rounds[node_name] == node_rounds[previous[node_name]] + 2:
                path.append(
                    (
                        f"{previous[node_name]}-{node_name}",
                        node_rounds[node_name] - 1,
                    )
                )
            node_name = previous[node_name]

        path.append((start.name, node_rounds[start.name]))
        path.reverse()

        return path
