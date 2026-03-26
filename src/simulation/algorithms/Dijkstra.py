import heapq
import logging
import math

from src.graph.Graph import Graph
from src.graph.node import Node
from src.graph.node.EndNode import EndNode
from src.graph.node.StartNode import StartNode


WAITING_DISCOUNT: float = (
    0.99  # Cost added when a drone waits at its current node
)
MAX_SIMULATION_TURNS: int = 200  # Hard cap on turns to prevent infinite loops
PRIORITY_ZONE_DISCOUNT: float = (
    0.80  # Reduced move cost to favour priority zones
)
RESTRICTED_ZONE_COST: float = (
    1.5  # Increased move cost to penalise restricted zones
)


class Dijkstra:
    """Time-expanded Dijkstra pathfinding algorithm.

    Operates on a space-time graph where each state is a ``(node, turn)``
    pair.  This allows the algorithm to respect dynamic node and link
    capacity constraints that vary per turn, enabling multi-drone routing
    without collision.
    """

    def __init__(self) -> None:
        """Initialize the Dijkstra algorithm with a named logger."""
        self.logger = logging.getLogger("Fly-In")

    def process(
        self,
        graph: Graph,
        occupancy: dict[int, dict[str, int]],
        link_occupancy: dict[int, dict[str, int]],
    ) -> dict[int, str]:
        """Run time-expanded Dijkstra for one drone.

        Explores ``(node_name, turn)`` states using a min-heap.  Capacity
        checks are performed at every step so that already-routed drones'
        occupancy is respected.

        Args:
            graph (Graph): The routing graph.
            occupancy (dict[int, dict[str, int]]): Node occupancy per turn
                from previously routed drones.
            link_occupancy (dict[int, dict[str, int]]): Link occupancy per
                turn from previously routed drones.

        Returns:
            dict[int, str]: Turn-to-position mapping.  Returns ``{}`` if
            no path exists within :data:`MAX_SIMULATION_TURNS`.
        """
        # distances[(node_name, turn)] -> best cumulative cost found so far
        distances: dict[tuple[str, int], float] = {}
        # previous[(node_name, turn)] -> predecessor (node_name, turn) state
        previous: dict[tuple[str, int], tuple[str, int]] = {}

        start_node = graph.nodes["start"]
        # Support both 'goal' and 'impossible_goal' map conventions
        end_name = "goal" if "goal" in graph.nodes else "impossible_goal"

        # Heap entries are (cumulative_cost, turn, node_name)
        queue: list[tuple[float, int, str]] = [(0.0, 0, start_node.name)]
        distances[(start_node.name, 0)] = 0.0
        # Tracks nodes that have already been expanded to avoid re-expanding
        traversed_node = []

        while queue:
            distance, turn, current_node_name = heapq.heappop(queue)

            if (current_node_name, turn) in distances:
                if distance > distances[(current_node_name, turn)]:
                    continue

            current_node = graph.nodes[current_node_name]
            if current_node.name == end_name:
                new_path = self.__make_path(
                    start_node.name, (current_node.name, turn), previous
                )
                return {k: new_path[k] for k in sorted(new_path)}

            if turn > MAX_SIMULATION_TURNS:
                continue

            for neighbor_node in current_node.connected_nodes:
                if (
                    neighbor_node.name == current_node.name
                    or neighbor_node.name in traversed_node
                ):
                    continue
                if neighbor_node.zone == "blocked":
                    continue

                arrival_t = turn + (
                    2 if neighbor_node.zone == "restricted" else 1
                )  # Restricted zones cost an extra turn to traverse

                # A drone cannot wait on a link mid-transit: only enter if
                # the destination node is guaranteed free at arrival.
                # If it is full, the drone must wait at the source instead.
                if not self.__check_capacity(
                    neighbor_node, arrival_t, occupancy, graph
                ):
                    continue

                if not self.__check_link_capacity(
                    current_node,
                    neighbor_node,
                    turn,
                    arrival_t,
                    link_occupancy,
                    graph,
                ):
                    continue

                if neighbor_node.zone == "priority":
                    move_cost = PRIORITY_ZONE_DISCOUNT
                elif neighbor_node.zone == "restricted":
                    move_cost = RESTRICTED_ZONE_COST
                else:
                    move_cost = 1.0

                new_distance = distance + move_cost
                if new_distance < distances.get(
                    (neighbor_node.name, arrival_t), math.inf
                ):
                    distances[(neighbor_node.name, arrival_t)] = (
                        new_distance
                    )
                    previous[(neighbor_node.name, arrival_t)] = (
                        current_node.name,
                        turn,
                    )
                    heapq.heappush(
                        queue,
                        (new_distance, arrival_t, neighbor_node.name),
                    )
                    traversed_node.append(current_node_name)

            wait_t = turn + 1
            if self.__check_capacity(current_node, wait_t, occupancy, graph):
                new_distance = distance + WAITING_DISCOUNT
                if new_distance < distances.get(
                    (current_node.name, wait_t), math.inf
                ):
                    distances[(current_node.name, wait_t)] = new_distance
                    previous[(current_node.name, wait_t)] = (
                        current_node.name,
                        turn,
                    )
                    heapq.heappush(
                        queue, (new_distance, wait_t, current_node.name)
                    )

        return {}

    def __check_capacity(
        self,
        node: Node,
        time: int,
        occupancy: dict[int, dict[str, int]],
        graph: Graph,
    ) -> bool:
        """Check whether ``node`` can accept one more drone at ``time``.

        Start and end nodes are exempt from capacity limits.

        Args:
            node (Node): The hub to check.
            time (int): The turn at which the drone would occupy the node.
            occupancy (dict[int, dict[str, int]]): Current occupancy map.
            graph (Graph): Not used directly; kept for API symmetry.

        Returns:
            bool: True if the node has capacity, False otherwise.
        """
        if isinstance(node, StartNode) or isinstance(node, EndNode):
            return True

        maximum_capacity = getattr(node, "max_drones", 1)
        current_occ = occupancy.get(time, {}).get(node.name, 0)
        return current_occ < maximum_capacity

    def __check_link_capacity(
        self,
        from_node: Node,
        to_node: Node,
        start_time: int,
        arrival_time: int,
        link_occupancy: dict[int, dict[str, int]],
        graph: Graph,
    ) -> bool:
        """Check whether the link between two nodes can be traversed.

        Counts combined occupancy for both directions of the link (since
        links are bidirectional) across every turn in the transit window.

        Args:
            from_node (Node): Departure hub.
            to_node (Node): Destination hub.
            start_time (int): Turn when the drone leaves ``from_node``.
            arrival_time (int): Turn when the drone arrives at ``to_node``.
            link_occupancy (dict[int, dict[str, int]]): Current link
                occupancy map.
            graph (Graph): Used to look up the link object and its capacity.

        Returns:
            bool: True if the link has capacity for this transit window.
        """
        # Look up link by canonical name, then by reversed name (bidirectional)
        link_name = f"{from_node.name}-{to_node.name}"
        reverse_link = f"{to_node.name}-{from_node.name}"

        link_obj = graph.links.get(link_name) or graph.links.get(reverse_link)
        if not link_obj:
            return True

        maximum_capacity = link_obj.max_drone or 1

        for time in range(start_time + 1, arrival_time + 1):
            current_occ = link_occupancy.get(time, {}).get(link_name, 0)
            current_occ += link_occupancy.get(time, {}).get(reverse_link, 0)
            if current_occ >= maximum_capacity:
                return False

        return True

    def __make_path(
        self,
        start_name: str,
        end_state: tuple[str, int],
        previous: dict[tuple[str, int], tuple[str, int]],
    ) -> dict[int, str]:
        """Reconstruct the full turn-to-position path by back-tracking.

        Handles both single-turn moves and two-turn restricted-zone
        transitions by inserting an intermediate ``'hub1-hub2'`` entry.

        Args:
            start_name (str): Name of the start node (backtracking stops
                here).
            end_state (tuple[str, int]): ``(node_name, turn)`` of the goal
                state.
            previous (dict): Predecessor map built during the search.

        Returns:
            dict[int, str]: Complete path from turn 0 to the goal.
        """

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
