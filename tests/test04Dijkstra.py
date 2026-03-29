from src.GraphBuilder import GraphBuilder
from src.graph.Graph import Graph
from src.parsing.models.ConnectionModel import ConnectionModel
from src.parsing.models.HubModel import HubModel
from src.parsing.models.MapModel import MapModel
from src.parsing.utils.Enum import HubTypeEnum, ZoneEnum
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


def create_complex_map_model() -> MapModel:
    start_hub = HubModel(
        name="start",
        hub_type=HubTypeEnum.START,
        pos=(0, 0),
        zone=ZoneEnum.NORMAL,
        color="green",
        max_drones=20,
    )

    end_hub = HubModel(
        name="goal",
        hub_type=HubTypeEnum.END,
        pos=(4, 0),
        zone=ZoneEnum.NORMAL,
        color="red",
        max_drones=20,
    )

    hubs = [
        HubModel(
            name="hub1",
            hub_type=HubTypeEnum.HUB,
            pos=(1, 0),
            zone=ZoneEnum.NORMAL,
            max_drones=3,
        ),
        HubModel(
            name="hub2",
            hub_type=HubTypeEnum.HUB,
            pos=(2, 1),
            zone=ZoneEnum.PRIORITY,
            color="gold",
            max_drones=2,
        ),
        HubModel(
            name="hub3",
            hub_type=HubTypeEnum.HUB,
            pos=(3, 0),
            zone=ZoneEnum.NORMAL,
            max_drones=4,
        ),
        HubModel(
            name="hub4",
            hub_type=HubTypeEnum.HUB,
            pos=(2, -1),
            zone=ZoneEnum.RESTRICTED,
            color="maroon",
            max_drones=1,
        ),
    ]

    connections = [
        ConnectionModel(zone1="start", zone2="hub1", max_link_capacity=5),
        ConnectionModel(zone1="hub1", zone2="hub2", max_link_capacity=2),
        ConnectionModel(zone1="hub1", zone2="hub3", max_link_capacity=3),
        ConnectionModel(zone1="hub1", zone2="hub4", max_link_capacity=1),
        ConnectionModel(zone1="hub2", zone2="hub3", max_link_capacity=2),
        ConnectionModel(zone1="hub4", zone2="hub3", max_link_capacity=1),
        ConnectionModel(zone1="hub3", zone2="goal", max_link_capacity=5),
    ]

    return MapModel(
        nb_drones=5,
        start_hub=start_hub,
        end_hub=end_hub,
        hubs=hubs,
        connections=connections,
    )


def build_graph(map: MapModel) -> Graph:
    builder = GraphBuilder()
    map_model = map

    return builder.build(map_model, "test_simple")


class TestDijkstra:
    algorithm = Dijkstra()
    graph_simple = build_graph(create_simple_map_model())
    graph_complex = build_graph(create_complex_map_model())

    def test_solo_drone_simple(self) -> None:
        path: dict[int, str] = self.algorithm.process(
            self.graph_simple, {}, {}
        )

        waiting_res = {
            0: "start",
            1: "hub1",
            2: "hub1-hub2",
            3: "hub2",
            4: "goal",
        }

        assert path == waiting_res

    def test_multi_drone_simple(self) -> None:
        occupancy: dict[int, dict[str, int]] = {}
        link_occupancy: dict[int, dict[str, int]] = {}
        all_paths: dict[int, dict[int, str]] = {}

        for drone in range(2):
            path: dict[int, str] = self.algorithm.process(
                self.graph_simple, occupancy, link_occupancy
            )
            if not path:
                continue
            for node_turn, node_name in path.items():
                tour_occ = occupancy.setdefault(node_turn, {})
                tour_occ[node_name] = tour_occ.get(node_name, 0) + 1

                if node_turn > 0 and "-" in node_name:
                    link_occ = link_occupancy.setdefault(node_turn, {})
                    link_occ[node_name] = link_occ.get(node_name, 0) + 1
            all_paths[drone + 1] = path

        waiting_res = {
            1: {0: "start", 1: "hub1", 2: "hub1-hub2", 3: "hub2", 4: "goal"},
            2: {
                0: "start",
                1: "start",
                2: "hub1",
                3: "hub1-hub2",
                4: "hub2",
                5: "goal",
            },
        }

        assert all_paths == waiting_res

    def test_solo_drone_complex(self) -> None:
        path: dict[int, str] = self.algorithm.process(
            self.graph_complex, {}, {}
        )

        waiting_res = {
            0: "start",
            1: "hub1",
            2: "hub3",
            3: "goal",
        }

        assert path == waiting_res

    def test_multi_drone_complex(self) -> None:
        occupancy: dict[int, dict[str, int]] = {}
        link_occupancy: dict[int, dict[str, int]] = {}
        all_paths: dict[int, dict[int, str]] = {}

        for drone in range(5):
            path: dict[int, str] = self.algorithm.process(
                self.graph_complex, occupancy, link_occupancy
            )
            if not path:
                continue
            for node_turn, node_name in path.items():
                tour_occ = occupancy.setdefault(node_turn, {})
                tour_occ[node_name] = tour_occ.get(node_name, 0) + 1

                if node_turn > 0 and "-" in node_name:
                    link_occ = link_occupancy.setdefault(node_turn, {})
                    link_occ[node_name] = link_occ.get(node_name, 0) + 1
            all_paths[drone + 1] = path

        waiting_res = {
            1: {0: "start", 1: "hub1", 2: "hub3", 3: "goal"},
            2: {0: "start", 1: "hub1", 2: "hub3", 3: "goal"},
            3: {0: "start", 1: "hub1", 2: "hub3", 3: "goal"},
            4: {0: "start", 1: "start", 2: "hub1", 3: "hub3", 4: "goal"},
            5: {0: "start", 1: "start", 2: "hub1", 3: "hub3", 4: "goal"},
        }

        assert all_paths == waiting_res
