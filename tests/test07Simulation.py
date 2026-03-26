import pytest

from src.GraphBuilder import GraphBuilder
from src.graph.Graph import Graph
from src.parsing.models.ConnectionModel import ConnectionModel
from src.parsing.models.HubModel import HubModel
from src.parsing.models.MapModel import MapModel
from src.parsing.utils.Enum import HubTypeEnum, ZoneEnum
from src.simulation.Simulation import Simulation
from src.simulation.algorithms.Dijkstra import Dijkstra


def create_simple_map_model() -> MapModel:
    start_hub = HubModel(
        name="start",
        hub_type=HubTypeEnum.START,
        pos=(0, 0),
        zone=ZoneEnum.NORMAL,
        color="green",
        max_drones=10,
    )

    end_hub = HubModel(
        name="goal",
        hub_type=HubTypeEnum.END,
        pos=(3, 0),
        zone=ZoneEnum.NORMAL,
        color="red",
        max_drones=10,
    )

    hub1 = HubModel(
        name="hub1",
        hub_type=HubTypeEnum.HUB,
        pos=(1, 0),
        zone=ZoneEnum.NORMAL,
        color="blue",
        max_drones=2,
    )

    hub2 = HubModel(
        name="hub2",
        hub_type=HubTypeEnum.HUB,
        pos=(2, 0),
        zone=ZoneEnum.RESTRICTED,
        color="orange",
        max_drones=1,
    )

    connections = [
        ConnectionModel(zone1="start", zone2="hub1", max_link_capacity=2),
        ConnectionModel(zone1="hub1", zone2="hub2", max_link_capacity=1),
        ConnectionModel(zone1="hub2", zone2="goal", max_link_capacity=3),
    ]

    return MapModel(
        nb_drones=2,
        start_hub=start_hub,
        end_hub=end_hub,
        hubs=[hub1, hub2],
        connections=connections,
    )


def build_graph(map: MapModel) -> Graph:
    builder = GraphBuilder()
    map_model = map

    return builder.build(map_model, "test_simple")


class TestSimulation:
    simulation = Simulation()
    graph: Graph = build_graph(create_simple_map_model())
    allpaths: dict[int, dict[int, str]] = {
        1: {0: "start", 1: "hub1", 2: "hub1-hub2", 3: "hub2", 4: "goal"},
        2: {0: "start", 2: "hub1", 3: "hub1-hub2", 4: "hub2", 5: "goal"},
        3: {0: "start", 3: "hub1", 4: "hub1-hub2", 5: "hub2", 6: "goal"},
        4: {0: "start", 4: "hub1", 5: "hub1-hub2", 6: "hub2", 7: "goal"},
        5: {0: "start", 5: "hub1", 6: "hub1-hub2", 7: "hub2", 8: "goal"},
    }

    def test_launch_simulation(self) -> None:
        allpaths, _, _ = self.simulation.start(Dijkstra(), self.graph, 5)
        assert allpaths == {
            1: {0: "start", 1: "hub1", 2: "hub1-hub2", 3: "hub2", 4: "goal"},
            2: {0: "start", 2: "hub1", 3: "hub1-hub2", 4: "hub2", 5: "goal"},
            3: {0: "start", 3: "hub1", 4: "hub1-hub2", 5: "hub2", 6: "goal"},
            4: {0: "start", 4: "hub1", 5: "hub1-hub2", 6: "hub2", 7: "goal"},
            5: {0: "start", 5: "hub1", 6: "hub1-hub2", 7: "hub2", 8: "goal"},
        }

    def test_format_output_correct(self) -> None:
        res = self.simulation._format_output(self.allpaths)
        assert res[0] == "D1-hub1"

    def test_format_output_empty_path(self) -> None:
        with pytest.raises(ValueError):
            self.simulation._compute_metrics({})

    def test_compute_metrics(self) -> None:
        res = self.simulation._compute_metrics(self.allpaths)

        assert res == {
            "total_turns": 8,
            "total_drones": 5,
            "avg_turns_per_drone": 5,
            "throughput": 5 / 8,
            "total_movements": 25,
        }
