from unittest.mock import MagicMock

import pytest

from src.simulation.PathfindingAlgorithm import PathfindingAlgorithm


class testPathfindingAlgorithm:
    factory = PathfindingAlgorithm()

    def test_create_dijkstra(self) -> None:
        assert self.factory.create("dijkstra")

    def test_unknown_algorithm(self) -> None:
        with pytest.raises(ValueError):
            self.factory.create("unknown")

    def register_new_algo(self) -> None:
        new_algo = MagicMock()
        assert self.factory.register("new_algo", new_algo)

    def register_bad_new_algo(self) -> None:
        with pytest.raises(TypeError):
            self.factory.register("new_algo", 45)  # type: ignore

    def test_get_available_algo(self) -> None:
        assert self.factory.get_available_algorithms() == ["dijkstra"]
