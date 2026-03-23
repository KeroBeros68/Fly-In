from src.simulation.algorithms.AlgorithmProtocol import AlgorithmProtocol


class PathfindingAlgorithm:
    __algorithms: dict[str, type[AlgorithmProtocol]] = {}

    @classmethod
    def _init_algorithms(cls) -> None:
        if not cls.__algorithms:
            try:
                from src.simulation.algorithms.Dijkstra import (
                    Dijkstra,
                )

                cls.__algorithms = {
                    "dijkstra": Dijkstra,
                }
            except ImportError as e:
                raise RuntimeError(
                    f"Failed to initialize algorithms: {e}"
                ) from e
            except Exception as e:
                raise RuntimeError(
                    f"Unexpected error during algorithm initialization: {e}"
                ) from e

    @classmethod
    def create(cls, algorithm_name: str) -> AlgorithmProtocol:
        cls._init_algorithms()
        algo_name_lower = algorithm_name.lower().strip()

        if algo_name_lower not in cls.__algorithms:
            available = ", ".join(cls.__algorithms.keys())
            raise ValueError(
                f"Algorithm '{algorithm_name}' not found. "
                f"Available algorithms: {available}"
            )

        algorithm_class = cls.__algorithms[algo_name_lower]
        return algorithm_class()

    @classmethod
    def register(
        cls, name: str, algorithm_class: type[AlgorithmProtocol]
    ) -> None:
        from src.simulation.algorithms.AlgorithmProtocol import (
            AlgorithmProtocol,
        )

        if not issubclass(algorithm_class, AlgorithmProtocol):
            raise TypeError(
                f"{algorithm_class.__name__} must implement AlgorithmProtocol"
            )

        cls._init_algorithms()
        cls.__algorithms[name.lower()] = algorithm_class

    @classmethod
    def get_available_algorithms(cls) -> list[str]:
        cls._init_algorithms()
        return list(cls.__algorithms.keys())
