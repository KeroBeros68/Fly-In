from src.simulation.algorithms.AlgorithmProtocol import AlgorithmProtocol


class PathfindingAlgorithm:
    """
    Registry and factory for pathfinding algorithm implementations.

    Provides class-level methods to register, instantiate, and list
    available algorithms by name.
    """

    __algorithms: dict[str, type[AlgorithmProtocol]] = {}

    @classmethod
    def _init_algorithms(cls) -> None:
        """
        Lazily initializes the algorithm registry with built-in algorithms.

        Raises:
            RuntimeError: If an algorithm import or initialization fails.
        """
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
        """
        Instantiates and returns the algorithm registered under the given name.

        Args:
            algorithm_name (str): Name of the algorithm (case-insensitive).

        Returns:
            AlgorithmProtocol: A new instance of the requested algorithm.

        Raises:
            ValueError: If no algorithm with that name is registered.
        """
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
        """
        Registers a new algorithm class under the given name.

        Args:
            name (str): The name key to register the algorithm under.
            algorithm_class (type[AlgorithmProtocol]): The algorithm class to
            register.

        Raises:
            TypeError: If the class does not implement AlgorithmProtocol.
        """
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
        """
        Returns a list of all registered algorithm names.

        Returns:
            list[str]: Names of available algorithms.
        """
        cls._init_algorithms()
        return list(cls.__algorithms.keys())
