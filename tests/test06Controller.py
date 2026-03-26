from collections.abc import Generator
from typing import Any

import pytest
from unittest.mock import MagicMock
from PySide6.QtWidgets import QApplication

from src.Controller import Controller, ControllerError
from src.graph.Graph import Graph
from src.parsing.errors.MapErrors import MapError


# Une seule QApplication par session de tests (PySide6 l'exige)
@pytest.fixture(scope="session")
def qt_app() -> Generator[Any, Any, Any]:
    app = QApplication.instance() or QApplication([])
    yield app


def make_controller() -> Any:
    mock_reader = MagicMock()
    mock_builder = MagicMock()
    mock_parser = MagicMock()
    mock_algorithm = MagicMock()
    mock_simulation = MagicMock()
    return Controller(
        mock_reader, mock_builder, mock_parser, mock_algorithm, mock_simulation
    )


class TestController:

    ctrl = make_controller()

    reader: Any = ctrl.reader
    parser: Any = ctrl.parser
    builder: Any = ctrl.builder
    engine: Any = ctrl.simulation_engine

    def setup_method(self) -> None:
        self.reader.reset_mock(side_effect=True, return_value=True)
        self.parser.reset_mock(side_effect=True, return_value=True)
        self.builder.reset_mock(side_effect=True, return_value=True)
        self.engine.reset_mock(side_effect=True, return_value=True)

    def test_load_file_empty_path_emits_false(
        self, qt_app: QApplication
    ) -> None:

        received: list[bool] = []
        self.ctrl.file_loaded.connect(lambda v: received.append(v))

        self.ctrl.load_file("")

        assert received == [False]
        self.reader.read_file.assert_not_called()

    def test_load_file_success_calls_pipeline(
        self, qt_app: QApplication
    ) -> None:

        self.reader.read_file.return_value = "nb_drones: 1\n..."
        mock_map_model = MagicMock()
        mock_map_model.nb_drones = 1
        self.parser.process.return_value = mock_map_model

        mock_graph = MagicMock(spec=Graph)
        self.builder.build.return_value = mock_graph

        self.engine.start.return_value = (
            {1: {0: "start", 1: "goal"}},
            ["D1-goal"],
            {},
        )

        loaded: list[bool] = []
        self.ctrl.file_loaded.connect(lambda v: loaded.append(v))

        self.ctrl.load_file("test.txt")

        self.reader.read_file.assert_called_once_with(
            "test.txt"
        )
        self.parser.process.assert_called_once()
        self.builder.build.assert_called_once()
        self.engine.start.assert_called_once()
        assert loaded == [True]

    def test_load_file_not_found_emits_error(
        self, qt_app: QApplication
    ) -> None:
        self.reader.read_file.side_effect = FileNotFoundError("no such file")

        errors: list[str] = []
        self.ctrl.file_error.connect(lambda msg: errors.append(msg))

        self.ctrl.load_file("nonexistent.txt")

        assert len(errors) == 1
        assert "no such file" in errors[0]
        self.parser.process.assert_not_called()

    def test_load_file_parse_error_emits_file_error(
        self, qt_app: QApplication
    ) -> None:
        self.reader.read_file.return_value = "contenu invalide"
        self.parser.process.side_effect = MapError("bad map")

        errors: list[str] = []
        self.ctrl.file_error.connect(lambda msg: errors.append(msg))

        self.ctrl.load_file("bad_map.txt")

        assert len(errors) == 1
        assert "bad map" in errors[0]
        self.builder.build.assert_not_called()
        self.engine.start.assert_not_called()

    def test_launch_simulation_emits_load_sim(
        self, qt_app: QApplication
    ) -> None:
        self.ctrl.graph = MagicMock(spec=Graph)
        self.ctrl.nb_drones = 2

        all_paths = {1: {0: "start", 1: "goal"}, 2: {0: "start", 1: "goal"}}
        self.engine.start.return_value = (
            all_paths,
            ["D1-goal D2-goal"],
            {},
        )

        sim_results: list[dict[int, dict[int, str]]] = []
        self.ctrl.load_sim.connect(lambda v: sim_results.append(v))

        self.ctrl.launch_simulation()

        self.engine.start.assert_called_once_with(
            self.ctrl.algorithm, self.ctrl.graph, 2
        )
        assert sim_results == [all_paths]

    def test_exit_program_raises_controller_error(
        self, qt_app: QApplication
    ) -> None:
        with pytest.raises(ControllerError):
            self.ctrl.exit_program()
