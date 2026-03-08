import pytest

from errors.MapErrors import (
    MapConnectionError,
    MapDuplicateHubError,
    MapInvalidCoordinatesError,
    MapMissingHubError,
)
from parsing import MapParser


class TestParser:
    NO_START: str = (
        "nb_drones: 2\n"
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

    def test_no_start(self):
        parser = MapParser(self.NO_START)
        try:
            parser.process()
            pytest.fail("INVALID[ No Start ]")
        except (
            MapMissingHubError,
        ):
            pass

    def test_no_end(self):
        parser = MapParser(self.NO_END)
        try:
            parser.process()
            pytest.fail("INVALID[ No End ]")
        except (
            MapMissingHubError,
        ):
            pass

    def test_pos_is_alpha(self):
        parser = MapParser(self.POS_IS_ALPHA)
        try:
            parser.process()
            pytest.fail("INVALID[ Pos is alpha ]")
        except (
            MapInvalidCoordinatesError,
        ):
            pass

    def test_dub_hub(self):
        parser = MapParser(self.DUP_HUB)
        try:
            parser.process()
            pytest.fail("INVALID[ Hub duplication ]")
        except (
            MapDuplicateHubError,
        ):
            pass

    def test_bad_hub_connection(self):
        parser = MapParser(self.BAD_HUB_CONNECTION)
        try:
            parser.process()
            pytest.fail("INVALID[ Bad hub connection ]")
        except (
            MapConnectionError,
        ):
            pass

    def test_miror_connection(self):
        parser = MapParser(self.MIRROR_CONNECTION)
        try:
            parser.process()
            pytest.fail("INVALID[ Mirror Connection ]")
        except (
            MapConnectionError,
        ):
            pass

    def test_max_link_connection(self):
        parser = MapParser(self.MAX_LINK_CONNECTION)
        try:
            parser.process()
            pytest.fail("INVALID[ Max link connection not a number ]")
        except (
            MapConnectionError,
        ):
            pass
