import logging

from src.graph.Graph import Graph
from src.graph.algorithms.Dijkstra import Dijkstra


class Simulation:
    def __init__(self) -> None:
        self.logger = logging.getLogger("Fly-In")

    def start(self, graph: Graph, nb_drone: int):
        algorithm = Dijkstra()
        occupancy: dict[int, dict[str, int]] = {}
        all_paths: dict[int, dict[int, str]] = {}
        for nb in range(nb_drone):
            path = algorithm.dijkstra(graph, occupancy)
            if not path:
                self.logger.error(
                    f"Drone {nb + 1} could not find a path!"
                )
                continue

            for node_turn, node_name in path.items():
                tour_occ = occupancy.setdefault(node_turn, {})
                tour_occ[node_name] = tour_occ.get(node_name, 0) + 1
            all_paths[nb + 1] = path

        for drone_id, path in all_paths.items():
            self.logger.info(f"{drone_id}: {path}")

        return all_paths
