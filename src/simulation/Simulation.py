import logging
from typing import Any

from src.graph.Graph import Graph
from src.simulation.algorithms.AlgorithmProtocol import AlgorithmProtocol


class Simulation:
    """
    Orchestrates the drone simulation by running a pathfinding algorithm
    for each drone and collecting their paths, output lines, and metrics.
    """

    def __init__(self) -> None:
        """Initializes the Simulation with a logger."""
        self.logger = logging.getLogger("Fly-In")

    def start(
        self, algorithm: AlgorithmProtocol, graph: Graph, number_of_drones: int
    ) -> tuple[dict[int, dict[int, str]], list[str], dict[str, str]]:
        """
        Runs the simulation for all drones using the provided algorithm.

        Args:
            algorithm (AlgorithmProtocol): The pathfinding algorithm to use
            per drone.
            graph (Graph): The graph on which drones travel.
            number_of_drones (int): Number of drones to simulate.

        Returns:
            tuple: A 3-tuple of:
                - all_paths (dict[int, dict[int, str]]): Per-drone
                turn-to-node mapping.
                - output_lines (list[str]): Formatted movement lines for each
                turn.
                - metrics (dict[str, str]): Simulation statistics.
        """
        # Tracks how many drones occupy each node per turn
        occupancy: dict[int, dict[str, int]] = {}
        # Tracks how many drones are in transit on each link per turn
        link_occupancy: dict[int, dict[str, int]] = {}
        # Maps each drone id to its full path (turn → node name)
        all_paths: dict[int, dict[int, str]] = {}
        for nb in range(number_of_drones):
            path = algorithm.process(graph, occupancy, link_occupancy)
            if not path:
                self.logger.error(f"Drone {nb + 1} could not find a path!")
                continue

            for node_turn, node_name in path.items():
                tour_occ = occupancy.setdefault(node_turn, {})
                tour_occ[node_name] = tour_occ.get(node_name, 0) + 1

                # Node names containing "-" represent in-transit positions on
                # a link
                if node_turn > 0 and "-" in node_name:
                    link_occ = link_occupancy.setdefault(node_turn, {})
                    link_occ[node_name] = link_occ.get(node_name, 0) + 1
            all_paths[nb + 1] = path

        for drone_id, path in all_paths.items():
            self.logger.info(f"{drone_id}: {path}")

        output_lines = self._format_output(all_paths)
        self.logger.info(output_lines)
        metrics = self._compute_metrics(all_paths)
        self.logger.info(metrics)

        return all_paths, output_lines, metrics

    def _format_output(
        self, all_paths: dict[int, dict[int, str]]
    ) -> list[str]:
        """
        Formats the simulation paths into human-readable output lines.

        Each line represents one turn and lists drone movements as
        'D{id}-{node}'.

        Args:
            all_paths (dict[int, dict[int, str]]): Per-drone turn-to-node
            mapping.

        Returns:
            list[str]: One string per turn describing all drone movements.
        """
        try:
            max_turn = max(max(path.keys()) for path in all_paths.values())
            output_lines = []

            for turn in range(1, max_turn + 1):
                movements = []
                for drone_id, path in all_paths.items():
                    if turn in path:
                        current_pos = path[turn]
                        prev_pos = path.get(turn - 1, "")
                        if current_pos != prev_pos:
                            movements.append(f"D{drone_id}-{current_pos}")

                if movements:
                    output_lines.append(" ".join(movements))

            return output_lines
        except (ValueError, AttributeError) as e:
            self.logger.warning(f"Format output error: {str(e)}")
            return []

    def _compute_metrics(
        self, all_paths: dict[int, dict[int, str]]
    ) -> dict[str, Any]:
        """
        Computes summary statistics from the completed simulation paths.

        Args:
            all_paths (dict[int, dict[int, str]]): Per-drone turn-to-node
            mapping.

        Returns:
            dict: A dictionary with keys: total_turns, total_drones,
                  avg_turns_per_drone, throughput, total_movements.
        """
        total_turns = max(max(path.keys()) for path in all_paths.values())
        total_drones = len(all_paths)
        total_moves = sum(
            len([k for k in path.keys() if path[k] != path.get(k - 1)])
            for path in all_paths.values()
        )

        return {
            "total_turns": total_turns,
            "total_drones": total_drones,
            "avg_turns_per_drone": sum(len(p) for p in all_paths.values())
            / total_drones,
            "throughput": total_drones / total_turns,
            "total_movements": total_moves,
        }
