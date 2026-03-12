from pydantic import ValidationError
import pytest

from src.parsing.errors.MapErrors import (
    MapConnectionError,
    MapDuplicateHubError,
    MapEmptyError,
    MapInvalidCoordinatesError,
    MapInvalidHubTypeError,
    MapMissingHubError,
    MapNbDronesError,
)
from src.parsing import MapParser


class TestParser:

    GOOD_MAP: str = (
        "nb_drones: 15\n"
        "start_hub: start 0 0 [color=green max_drones=15]\n"
        "hub: dist_gate1 1 0 [color=orange max_drones=1]\n"
        "hub: dist_gate2 1 1 [color=orange max_drones=1]\n"
        "hub: dist_gate3 1 -1 [color=orange max_drones=1]\n"
        "hub: maze_trap1 2 2 [color=red]\n"
        "hub: maze_loop1 2 1 [zone=restricted color=purple]\n"
        "hub: maze_correct 2 0 [color=blue]\n"
        "hub: bottleneck1 3 0 [color=yellow max_drones=2]\n"
        "hub: overflow1 3 -1 [zone=restricted color=orange max_drones=3]\n"
        "hub: priority_hub 5 0 [zone=priority color=cyan max_drones=4]\n"
        "hub: final_merge 9 0 [color=magenta max_drones=8]\n"
        "hub: final_gate1 10 0 [color=orange max_drones=3]\n"
        "hub: final_gate2 11 0 [color=orange max_drones=2]\n"
        "hub: final_gate3 12 0 [color=orange max_drones=1]\n"
        "end_hub: goal 13 0 [color=gold max_drones=15]\n"
        "connection: start-dist_gate1\n"
        "connection: start-dist_gate2\n"
        "connection: start-dist_gate3\n"
        "connection: dist_gate1-maze_correct\n"
        "connection: dist_gate2-maze_loop1\n"
        "connection: dist_gate3-overflow1\n"
        "connection: maze_correct-bottleneck1\n"
        "connection: maze_loop1-maze_correct\n"
        "connection: maze_trap1-maze_loop1\n"
        "connection: bottleneck1-priority_hub\n"
        "connection: overflow1-bottleneck1\n"
        "connection: priority_hub-final_merge\n"
        "connection: final_merge-final_gate1\n"
        "connection: final_merge-final_gate2\n"
        "connection: final_merge-final_gate3\n"
        "connection: final_gate1-goal\n"
        "connection: final_gate2-goal\n"
        "connection: final_gate3-goal\n"
    )

    EMPTY_MAP: str = ""

    NO_DRONE_LINE: str = (
        "start_hub: start 0 0 [color=green max_drones=15]\n"
        "hub: dist_gate1 1 0 [color=orange max_drones=1]\n"
        "end_hub: goal 13 0 [color=gold max_drones=15]\n"
        "connection: start-dist_gate1\n"
        "connection: dist_gate1-goal\n"
    )

    ZERO_DRONE: str = (
        "nb_drones: 0\n"
        "start_hub: start 0 0 [color=green max_drones=15]\n"
        "hub: dist_gate1 1 0 [color=orange max_drones=1]\n"
        "end_hub: goal 13 0 [color=gold max_drones=15]\n"
        "connection: start-dist_gate1\n"
        "connection: dist_gate1-goal\n"
    )

    NO_DRONE: str = (
        "nb_drones: \n"
        "start_hub: start 0 0 [color=green max_drones=15]\n"
        "hub: dist_gate1 1 0 [color=orange max_drones=1]\n"
        "end_hub: goal 13 0 [color=gold max_drones=15]\n"
        "connection: start-dist_gate1\n"
        "connection: dist_gate1-goal\n"
    )

    NO_START: str = (
        "nb_drones: 2\n"
        "hub: start 0 0 [color=green]\n"
        "hub: waypoint1 1 0 [color=blue]\n"
        "end_hub: goal 3 0 [color=red]\n"
        "connection: start-waypoint1\n"
    )

    DUP_START: str = (
        "nb_drones: 2\n"
        "start_hub: start 0 0 [color=green]\n"
        "start_hub: start 0 0 [color=green]\n"
        "hub: start 0 0 [color=green]\n"
        "hub: waypoint1 1 0 [color=blue]\n"
        "end_hub: goal 3 0 [color=red]\n"
        "connection: start-waypoint1\n"
    )

    NO_END: str = (
        "nb_drones: 2\n"
        "start_hub: start 0 0 [color=green]\n"
        "hub: waypoint1 1 0 [color=blue]\n"
        "connection: start-waypoint1\n"
    )

    POS_IS_ALPHA: str = (
        "nb_drones: 2\n"
        "start_hub: start b 0 [color=green]\n"
        "hub: waypoint1 1 0 [color=blue]\n"
        "end_hub: goal 3 0 [color=red]\n"
        "connection: start-waypoint1\n"
    )

    INVALID_HUB_TYPE: str = (
        "nb_drones: 2\n"
        "start_hub: start 0 0 [color=green]\n"
        "Doomed: waypoint1 1 0 [color=blue]\n"
        "hub: waypoint1 1 0 [color=blue]\n"
        "end_hub: goal 3 0 [color=red]\n"
        "connection: start-waypoint1\n"
    )

    DUP_HUB: str = (
        "nb_drones: 2\n"
        "start_hub: start 0 0 [color=green]\n"
        "hub: waypoint1 1 0 [color=blue]\n"
        "hub: waypoint1 1 0 [color=blue]\n"
        "end_hub: goal 3 0 [color=red]\n"
        "connection: start-waypoint1\n"
    )

    BAD_HUB_CONNECTION: str = (
        "nb_drones: 2\n"
        "start_hub: start 0 0 [color=green]\n"
        "hub: waypoint1 1 0 [color=blue]\n"
        "end_hub: goal 3 0 [color=red]\n"
        "connection: start-waypoint2\n"
    )

    MIRROR_CONNECTION: str = (
        "nb_drones: 2\n"
        "start_hub: start 0 0 [color=green]\n"
        "hub: waypoint1 1 0 [color=blue]\n"
        "end_hub: goal 3 0 [color=red]\n"
        "connection: start-waypoint1 [max_link_capacity=1]\n"
        "connection: waypoint1-start [max_link_capacity=1]\n"
    )

    MAX_LINK_CONNECTION: str = (
        "nb_drones: 2\n"
        "start_hub: start 0 0 [color=green]\n"
        "hub: waypoint1 1 0 [color=blue]\n"
        "end_hub: goal 3 0 [color=red]\n"
        "connection: start-waypoint1 [max_link_capacity=banane]\n"
    )

    def test_good_map(self) -> None:
        parser = MapParser(self.GOOD_MAP)
        result = parser.process()
        assert result.nb_drones == 15
        assert result.start_hub.name == "start"
        assert result.end_hub.name == "goal"
        assert len(result.hubs) == 13
        assert len(result.connections) == 18

    def test_empty_map(self) -> None:
        parser = MapParser(self.EMPTY_MAP)
        try:
            parser.process()
            pytest.fail("INVALID[ Empty map ]")
        except MapEmptyError:
            pass

    def test_no_drone_line(self) -> None:
        parser = MapParser(self.NO_DRONE_LINE)
        try:
            parser.process()
            pytest.fail("INVALID[ No drone line ]")
        except MapNbDronesError:
            pass

    def test_zero_drone(self) -> None:
        parser = MapParser(self.ZERO_DRONE)
        try:
            parser.process()
            pytest.fail("INVALID[ Zero Drone ]")
        except ValidationError:
            pass

    def test_no_drone(self) -> None:
        parser = MapParser(self.NO_DRONE)
        try:
            parser.process()
            pytest.fail("INVALID[ No Drone ]")
        except MapNbDronesError:
            pass

    def test_no_start(self) -> None:
        parser = MapParser(self.NO_START)
        try:
            parser.process()
            pytest.fail("INVALID[ No Start ]")
        except (MapMissingHubError,):
            pass

    def test_dup_start(self) -> None:
        parser = MapParser(self.DUP_START)
        try:
            parser.process()
            pytest.fail("INVALID[ Dup Start ]")
        except (MapDuplicateHubError,):
            pass

    def test_no_end(self) -> None:
        parser = MapParser(self.NO_END)
        try:
            parser.process()
            pytest.fail("INVALID[ No End ]")
        except (MapMissingHubError,):
            pass

    def test_pos_is_alpha(self) -> None:
        parser = MapParser(self.POS_IS_ALPHA)
        try:
            parser.process()
            pytest.fail("INVALID[ Pos is alpha ]")
        except (MapInvalidCoordinatesError,):
            pass

    def test_invalid_hub_type(self) -> None:
        parser = MapParser(self.INVALID_HUB_TYPE)
        try:
            parser.process()
            pytest.fail("INVALID[ Hub type error]")
        except (MapInvalidHubTypeError,):
            pass

    def test_dub_hub(self) -> None:
        parser = MapParser(self.DUP_HUB)
        try:
            parser.process()
            pytest.fail("INVALID[ Hub duplication ]")
        except (MapDuplicateHubError,):
            pass

    def test_bad_hub_connection(self) -> None:
        parser = MapParser(self.BAD_HUB_CONNECTION)
        try:
            parser.process()
            pytest.fail("INVALID[ Bad hub connection ]")
        except (MapConnectionError,):
            pass

    def test_miror_connection(self) -> None:
        parser = MapParser(self.MIRROR_CONNECTION)
        try:
            parser.process()
            pytest.fail("INVALID[ Mirror Connection ]")
        except (MapConnectionError,):
            pass

    def test_max_link_connection(self) -> None:
        parser = MapParser(self.MAX_LINK_CONNECTION)
        try:
            parser.process()
            pytest.fail("INVALID[ Max link connection not a number ]")
        except (MapConnectionError,):
            pass
