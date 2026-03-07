from pydantic import ValidationError
import pytest

from errors.MapErrors import (
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

    def test_no_start(self):
        try:
            MapParser.process(self.NO_START)
            pytest.fail("INVALID[ No Start ]")
        except (
            MapMissingHubError,
        ):
            pass

    def test_no_end(self):
        try:
            MapParser.process(self.NO_END)
            pytest.fail("INVALID[ No End ]")
        except (
            MapMissingHubError,
        ):
            pass

    def test_pos_is_alpha(self):
        try:
            MapParser.process(self.POS_IS_ALPHA)
            pytest.fail("INVALID[ Pos is alpha ]")
        except (
            MapInvalidCoordinatesError,
        ):
            pass
