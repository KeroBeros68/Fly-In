import logging

from src.graph.Graph import Graph
from src.simulation.algorithms.AlgorithmProtocol import AlgorithmProtocol


class Simulation:
    def __init__(self) -> None:
        self.logger = logging.getLogger("Fly-In")

    def start(
        self, algorithm: AlgorithmProtocol, graph: Graph, number_of_drones: int
    ) -> tuple[dict[int, dict[int, str]], list[str]]:
        occupancy: dict[int, dict[str, int]] = {}
        link_occupancy: dict[int, dict[str, int]] = {}
        all_paths: dict[int, dict[int, str]] = {}
        for nb in range(number_of_drones):
            path = algorithm.process(graph, occupancy, link_occupancy)
            if not path:
                self.logger.error(f"Drone {nb + 1} could not find a path!")
                continue

            for node_turn, node_name in path.items():
                tour_occ = occupancy.setdefault(node_turn, {})
                tour_occ[node_name] = tour_occ.get(node_name, 0) + 1

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

        return all_paths, output_lines

    def _format_output(
        self, all_paths: dict[int, dict[int, str]]
    ) -> list[str]:
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

    def _compute_metrics(self, all_paths: dict[int, dict[int, str]]) -> dict:
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
