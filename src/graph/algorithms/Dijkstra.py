import heapq
import logging
import math

from src.graph.Graph import Graph
from src.graph.node import Node


class Dijkstra:
    def __init__(self) -> None:
        self.logger = logging.getLogger("Fly-In")

    def dijkstra(
        self, graph: Graph, occupancy: dict[int, dict[str, int]]
    ) -> dict[int, str]:

        distances: dict[tuple[str, int], float] = {}
        previous: dict[tuple[str, int], tuple[str, int]] = {}

        start_node = graph.nodes["start"]
        end_name = "goal" if "goal" in graph.nodes else "impossible_goal"

        # heapq: (cost, current_time, node_object)
        queue: list[tuple[float, int, str]] = [(0.0, 0, start_node.name)]
        distances[(start_node.name, 0)] = 0.0

        while queue:
            dist, t, u_name = heapq.heappop(queue)
            u = graph.nodes[u_name]
            if u.name == end_name:
                new_path = self.__make_path(
                    start_node.name, (u.name, t), previous
                )
                return {k: new_path[k] for k in sorted(new_path)}

            # Limite de sécurité pour éviter les boucles infinies en cas de
            # blocage total
            if t > 200:
                continue

            # --- OPTION 1 : Se déplacer vers un voisin ---
            for v in u.connected_nodes:
                if v.name == u.name:
                    continue  # On gère l'attente séparément
                if v.zone == "blocked":
                    continue

                arrival_t = t + (2 if v.zone == "restricted" else 1)

                if self.__check_capacity(v, arrival_t, occupancy, graph):
                    move_cost = 0.99 if v.zone == "priority" else 1.0
                    if v.zone == "restricted":
                        move_cost = 2.0

                    new_dist = dist + move_cost
                    if new_dist < distances.get((v.name, arrival_t), math.inf):
                        distances[(v.name, arrival_t)] = new_dist
                        previous[(v.name, arrival_t)] = (u.name, t)
                        heapq.heappush(queue, (new_dist, arrival_t, v.name))

            # --- OPTION 2 : Attendre sur place (Wait) ---
            # Le coût d'attente est de 1.0 tour.
            # On vérifie la capacité du nœud actuel au tour suivant.
            wait_t = t + 1
            if self.__check_capacity(u, wait_t, occupancy, graph):
                new_dist = (
                    dist + 1.05
                )  # Légère pénalité pour préférer bouger si possible
                if new_dist < distances.get((u.name, wait_t), math.inf):
                    distances[(u.name, wait_t)] = new_dist
                    previous[(u.name, wait_t)] = (u.name, t)
                    heapq.heappush(queue, (new_dist, wait_t, u.name))

        return {}

    def __check_capacity(
        self,
        node: Node,
        time: int,
        occupancy: dict[int, dict[str, int]],
        graph: Graph,
    ) -> bool:
        if node.type in ["start_hub", "goal_hub"]:
            return True

        max_cap = getattr(node, "max_drones", 1)

        current_occ = occupancy.get(time, {}).get(node.name, 0)
        return current_occ < max_cap

    def __make_path(
        self,
        start_name: str,
        end_state: tuple[str, int],
        previous: dict[tuple[str, int], tuple[str, int]],
    ) -> dict[int, str]:

        path: dict[int, str] = {}

        curr_name, curr_turn = end_state
        while curr_name != start_name:
            path[curr_turn] = curr_name
            prev_name, prev_turn = previous[(curr_name, curr_turn)]
            if curr_turn - prev_turn == 2:
                path[curr_turn - 1] = f"{prev_name}-{curr_name}"
            else:
                while curr_turn - prev_turn != 1:
                    curr_turn -= 1
                    path[curr_turn] = curr_name
            curr_name, curr_turn = prev_name, prev_turn

        path[0] = start_name
        return path
