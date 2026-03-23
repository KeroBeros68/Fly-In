import logging
import sys

from src.FileLoader import FileLoader
from src.GraphBuilder import GraphBuilder
from src.graph.Graph import Graph
from src.parsing.MapParser import MapParser
from src.simulation.Simulation import Simulation
from src.simulation.algorithms.AlgorithmProtocol import AlgorithmProtocol
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
    Main controller for managing the map parsing and simulation.

    Attributes:
        map_path (str): Path to the map to process.
        drone_list (list): List of initialized drones.
    """

    file_error = Signal(str)
    file_loaded = Signal(bool)
    load_graph = Signal(object)
    load_sim = Signal(object)

    def __init__(
        self,
        reader: FileLoader,
        builder: GraphBuilder,
        parser: MapParser,
        algorithm: AlgorithmProtocol,
        simulation: Simulation,
    ) -> None:
        """
        Initializes the Controller.

        Args:
            map_path (str): The path to the map configuration file.
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
        if path == "":
            self.file_loaded.emit(False)
            return
        self.map_name: str = path.split("/")[::-1][0].split(".")[0]
        self.logger.info(f"File received: {path}")

        try:
            content = self.reader.read_file(path)
            if content.startswith("File: "):
                self.file_error.emit(content)
                return
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

    def launch_simulation(self) -> None:
        """
        Initializes the simulation by instantiating drones.

        Args:
            nb_drone (int): The number of drones to initialize.
            start_pos (Tuple[int, int]): Drone start coordinates (x, y).
        """
        self.logger.info("Launch Simulation Start")
        all_paths = self.simulation_engine.start(
            self.algorithm, self.graph, self.nb_drones
        )
        self.logger.info("Launch Simulation Stop")
        self.load_sim.emit(all_paths)

    def exit_program(self) -> None:
        """
        Safely halts execution and exits the program.

        Raises:
            ControllerError: To break execution explicitly.
        """
        self.logger.info("Programm exit")
        raise ControllerError("Programm exit")
