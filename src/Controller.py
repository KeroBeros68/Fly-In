import logging
import sys

from src.FileLoader import FileLoader
from src.GraphBuilder import GraphBuilder
from src.graph.Graph import Graph
from src.parsing.MapParser import MapParser
from src.simulation.Simulation import Simulation
from src.simulation.algorithms.AlgorithmProtocol import AlgorithmProtocol
from src.utils.PausingArgumentParser import PausingArgumentParser
from src.view.ViewApp import ViewApp

from PySide6.QtCore import QObject, Signal

from src.parsing.errors.MapErrors import MapError


class ControllerError(Exception):
    """
    Exception raised for errors in the Controller.
    """

    def __init__(self, message: str) -> None:
        """
        Initializes the ControllerError.

        Args:
            message (str): The error message.
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """
        Returns the string representation of the error.

        Returns:
            str: The formatted error message.
        """
        return f"[ControllerError] {self.message}"


class Controller(QObject):
    """
    Main application controller managing map loading and simulation flow.

    Emits Qt signals to communicate state changes to the view layer.

    Signals:
        file_error (str): Emitted when a file loading error occurs.
        file_loaded (bool): Emitted when a file is successfully loaded or
                                                                        fails.
        load_graph (object): Emitted with the constructed Graph after loading.
        load_sim (object): Emitted with simulation paths after simulation runs.
        load_metrics (object): Emitted with simulation metrics after
                                                            simulation runs.
    """

    file_error = Signal(str)
    file_loaded = Signal(bool)
    load_graph = Signal(object)
    load_sim = Signal(object)
    load_metrics = Signal(object)

    def __init__(
        self,
        arg_parser: PausingArgumentParser,
        reader: FileLoader,
        builder: GraphBuilder,
        parser: MapParser,
        algorithm: AlgorithmProtocol,
        simulation: Simulation,
    ) -> None:
        """
        Initializes the Controller with its required dependencies.

        Args:
            arg_parser (PausingArgumentParser): Argument parser used to
                handle CLI arguments without exiting on error.
            reader (FileLoader): Used to read map files from disk.
            builder (GraphBuilder): Converts parsed map data into a Graph.
            parser (MapParser): Parses raw map file content into a MapModel.
            algorithm (AlgorithmProtocol): Pathfinding algorithm for the
                                                                simulation.
            simulation (Simulation): Simulation engine that runs the algorithm.
        """
        super().__init__()
        self.logger = logging.getLogger("Fly-In")
        self.reader: FileLoader = reader
        self.builder: GraphBuilder = builder
        self.parser: MapParser = parser
        self.algorithm: AlgorithmProtocol = algorithm
        self.simulation_engine: Simulation = simulation
        self.graph: Graph
        self.nb_drones: int = 0

    def process(self) -> None:
        """
        Executes the main controller flow.

        Reads the map file, parses its content, and initializes
        the simulation. Validates the secure environment if provided.
        """
        self.logger.info("Programm starting")
        try:
            self.app = ViewApp(self)
        except Exception as e:
            raise e

        sys.exit(self.app.app.exec())

    def load_file(self, path: str) -> None:
        """
        Loads, parses, and builds the graph from the given file path.

        Emits file_loaded and load_graph signals on success,
        or file_error on failure.

        Args:
            path (str): Path to the map file to load. Empty string is ignored.
        """
        if path == "":
            self.file_loaded.emit(False)
            return
        self.map_name: str = path.split("/")[::-1][0].split(".")[0]
        self.logger.info(f"File received: {path}")

        try:
            content = self.reader.read_file(path)

            if content != "":
                self.logger.info(content)
                try:
                    map_model = self.parser.process(content)
                except MapError as e:
                    self.logger.error(f"{e}")
                    self.file_error.emit(f"Error: {e}")
                    return

            if map_model:
                self.graph = self.builder.build(map_model, self.map_name)
                self.load_graph.emit(self.graph)
                self.nb_drones = map_model.nb_drones
                self.logger.info("File successfully loaded")
                self.file_loaded.emit(True)
                self.launch_simulation()
            else:
                self.logger.info("File not loaded")
                self.file_loaded.emit(False)
        except MapError as e:
            self.file_loaded.emit(False)
            self.logger.error(f"Error loading file: {e}")
        except (FileNotFoundError, PermissionError) as e:
            self.logger.error(f"File: {e}")
            self.file_error.emit(str(e))

    def launch_simulation(self) -> None:
        """
        Runs the simulation using the loaded graph and drone count.

        Emits load_sim with all drone paths and load_metrics with statistics.
        """
        self.logger.info("Launch Simulation Start")
        all_paths, output_lines, metrics = self.simulation_engine.start(
            self.algorithm, self.graph, self.nb_drones
        )
        self.logger.info("Launch Simulation Stop")
        self.load_sim.emit(all_paths)
        self.load_metrics.emit(metrics)

    def exit_program(self) -> None:
        """
        Safely halts execution and exits the program.

        Raises:
            ControllerError: To break execution explicitly.
        """
        self.logger.info("Programm exit")
        raise ControllerError("Programm exit")
