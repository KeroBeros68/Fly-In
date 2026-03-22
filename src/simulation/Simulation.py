import logging

from src.graph.Graph import Graph
from src.graph.algorithms.Dijkstra import Dijkstra
from src.simulation.drone.Drone import Drone


class Simulation():
    def __init__(self) -> None:
        self.drone_list: list[Drone] = []
        self.logger = logging.getLogger("Fly-In")

    def start(self, graph: Graph, nb_drone: int):
        self.drone_list = []
        all_path: dict[int, list[tuple[str, int]]] = {}
        for nb in range(nb_drone):
            self.drone_list.append(Drone(nb + 1, graph.nodes["start"].pos))
        self.logger.info("All drones initialized")
        for d in self.drone_list:
            valueTest = Dijkstra.dijkstra(graph)
            all_path[d.drone_id] = valueTest
        self.logger.warning(all_path)
        return all_path
