from src.GraphBuilder import GraphBuilder
from src.parsing.models.MapModel import MapModel
from src.parsing.models.HubModel import HubModel
from src.parsing.models.ConnectionModel import ConnectionModel
from src.parsing.utils.Enum import ZoneEnum, HubTypeEnum


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
        nb_drones=5,
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
        nb_drones=10,
        start_hub=start_hub,
        end_hub=end_hub,
        hubs=hubs,
        connections=connections,
    )


class TestBuilder:
    def test_build_simple_graph(self) -> None:
        builder = GraphBuilder()
        map_model = create_simple_map_model()

        graph = builder.build(map_model, "test_simple")

        assert graph.name == "test_simple"

        assert "start" in graph.nodes
        assert "goal" in graph.nodes
        assert "hub1" in graph.nodes
        assert "hub2" in graph.nodes
        assert len(graph.nodes) == 4

        assert graph.nodes["start"].__class__.__name__ == "StartNode"
        assert graph.nodes["goal"].__class__.__name__ == "EndNode"
        assert graph.nodes["hub1"].__class__.__name__ == "HubNode"

    def test_build_graph_nodes_positions(self) -> None:
        builder = GraphBuilder()
        map_model = create_simple_map_model()

        graph = builder.build(map_model, "test_positions")

        assert graph.nodes["start"].pos == (0, 0)
        assert graph.nodes["goal"].pos == (3, 0)
        assert graph.nodes["hub1"].pos == (1, 0)
        assert graph.nodes["hub2"].pos == (2, 0)

    def test_build_graph_nodes_zones(self) -> None:
        builder = GraphBuilder()
        map_model = create_simple_map_model()

        graph = builder.build(map_model, "test_zones")

        assert graph.nodes["start"].zone == "normal"
        assert graph.nodes["hub2"].zone == "restricted"

    def test_build_graph_nodes_max_drones(self) -> None:
        builder = GraphBuilder()
        map_model = create_simple_map_model()

        graph = builder.build(map_model, "test_capacity")

        assert graph.nodes["hub1"].max_drones == 2
        assert graph.nodes["hub2"].max_drones == 1

    def test_build_graph_connections(self) -> None:
        builder = GraphBuilder()
        map_model = create_simple_map_model()

        graph = builder.build(map_model, "test_connections")

        start_neighbors = [
            n.name for n in graph.nodes["start"].connected_nodes
        ]
        assert "hub1" in start_neighbors

        hub1_neighbors = [n.name for n in graph.nodes["hub1"].connected_nodes]
        hub2_neighbors = [n.name for n in graph.nodes["hub2"].connected_nodes]
        assert "hub2" in hub1_neighbors
        assert "hub1" in hub2_neighbors

    def test_build_graph_links(self) -> None:
        builder = GraphBuilder()
        map_model = create_simple_map_model()

        graph = builder.build(map_model, "test_links")

        assert len(graph.links) == 3

        link_names = list(graph.links.keys())
        assert any("start" in name and "hub1" in name for name in link_names)
        assert any("hub1" in name and "hub2" in name for name in link_names)
        assert any("hub2" in name and "goal" in name for name in link_names)

    def test_build_complex_graph(self) -> None:
        builder = GraphBuilder()
        map_model = create_complex_map_model()

        graph = builder.build(map_model, "test_complex")

        assert len(graph.nodes) == 6

        assert len(graph.links) == 7

        hub1_neighbors = [n.name for n in graph.nodes["hub1"].connected_nodes]
        assert len(hub1_neighbors) >= 3

    def test_build_graph_colors(self) -> None:
        builder = GraphBuilder()
        map_model = create_simple_map_model()

        graph = builder.build(map_model, "test_colors")

        assert graph.nodes["start"].color == "green"
        assert graph.nodes["goal"].color == "red"
        assert graph.nodes["hub1"].color == "blue"
        assert graph.nodes["hub2"].color == "orange"

    def test_build_graph_empty_hubs(self) -> None:
        start_hub = HubModel(
            name="start",
            hub_type=HubTypeEnum.START,
            pos=(0, 0),
            zone=ZoneEnum.NORMAL,
            max_drones=5,
        )

        end_hub = HubModel(
            name="goal",
            hub_type=HubTypeEnum.END,
            pos=(1, 0),
            zone=ZoneEnum.NORMAL,
            max_drones=5,
        )

        connections = [
            ConnectionModel(zone1="start", zone2="goal", max_link_capacity=1)
        ]

        map_model = MapModel(
            nb_drones=3,
            start_hub=start_hub,
            end_hub=end_hub,
            hubs=[],
            connections=connections,
        )

        builder = GraphBuilder()
        graph = builder.build(map_model, "test_empty")

        assert len(graph.nodes) == 2
        assert "start" in graph.nodes
        assert "goal" in graph.nodes

        assert len(graph.links) == 1
