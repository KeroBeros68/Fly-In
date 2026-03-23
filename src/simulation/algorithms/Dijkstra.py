import heapq
import logging
import math

from src.graph.Graph import Graph
from src.graph.node import Node


WAITING_PENALTY: float = 1.05  # Penalty to discourage waiting
MAX_SIMULATION_TURNS: int = 200  # Safety limit for infinite loops
PRIORITY_ZONE_DISCOUNT: float = 0.99  # Small discount for priority zones
RESTRICTED_ZONE_DISCOUNT: float = 1.00


class Dijkstra:
    def __init__(self) -> None:
        self.logger = logging.getLogger("Fly-In")

    def process(
        self,
        graph: Graph,
        occupancy: dict[int, dict[str, int]],
        link_occupancy: dict[int, dict[str, int]]
    ) -> dict[int, str]:

        distances: dict[tuple[str, int], float] = {}
        previous: dict[tuple[str, int], tuple[str, int]] = {}

        start_node = graph.nodes["start"]
        end_name = "goal" if "goal" in graph.nodes else "impossible_goal"

        queue: list[tuple[float, int, str]] = [(0.0, 0, start_node.name)]
        distances[(start_node.name, 0)] = 0.0

        while queue:
            dist, turn, current_node_name = heapq.heappop(queue)
            current_node = graph.nodes[current_node_name]
            if current_node.name == end_name:
                new_path = self.__make_path(
                    start_node.name, (current_node.name, turn), previous
                )
                return {k: new_path[k] for k in sorted(new_path)}

            if turn > MAX_SIMULATION_TURNS:
                continue

            for neighbor_node in current_node.connected_nodes:
                if neighbor_node.name == current_node.name:
                    continue
                if neighbor_node.zone == "blocked":
                    continue

                arrival_t = turn + (
                    2 if neighbor_node.zone == "restricted" else 1
                )

                if not self.__check_link_capacity(
                    current_node, neighbor_node, turn, arrival_t,
                    link_occupancy, graph
                ):
                    continue

                if self.__check_capacity(
                    neighbor_node, arrival_t, occupancy, graph
                ):
                    if neighbor_node.zone == "priority":
                        move_cost = PRIORITY_ZONE_DISCOUNT
                    elif neighbor_node.zone == "restricted":
                        move_cost = RESTRICTED_ZONE_DISCOUNT
                    else:
                        move_cost = 1.0

                    new_dist = dist + move_cost
                    if new_dist < distances.get(
                        (neighbor_node.name, arrival_t), math.inf
                    ):
                        distances[(neighbor_node.name, arrival_t)] = new_dist
                        previous[(neighbor_node.name, arrival_t)] = (
                            current_node.name,
                            turn,
                        )
                        heapq.heappush(
                            queue, (new_dist, arrival_t, neighbor_node.name)
                        )

            wait_t = turn + 1
            if self.__check_capacity(current_node, wait_t, occupancy, graph):
                new_dist = dist + WAITING_PENALTY
                if new_dist < distances.get(
                    (current_node.name, wait_t), math.inf
                ):
                    distances[(current_node.name, wait_t)] = new_dist
                    previous[(current_node.name, wait_t)] = (
                        current_node.name,
                        turn,
                    )
                    heapq.heappush(
                        queue, (new_dist, wait_t, current_node.name)
                    )

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

    def __check_link_capacity(
        self,
        from_node: Node,
        to_node: Node,
        start_time: int,
        arrival_time: int,
        link_occupancy: dict[int, dict[str, int]],
        graph: Graph,
    ) -> bool:
        link_name = f"{from_node.name}-{to_node.name}"
        reverse_link = f"{to_node.name}-{from_node.name}"

        link_obj = graph.links.get(link_name) or graph.links.get(reverse_link)
        if not link_obj:
            return True

        max_capacity = link_obj.max_drone or 1

        for time in range(start_time + 1, arrival_time + 1):
            current_occ = link_occupancy.get(time, {}).get(link_name, 0)
            current_occ += link_occupancy.get(time, {}).get(reverse_link, 0)
            if current_occ >= max_capacity:
                return False

        return True

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
