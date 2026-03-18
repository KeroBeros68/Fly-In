import logging
import sys
from typing import Tuple

from src.graph.Graph import Graph
from src.graph.algorithms.Dijkstra import Djikstra
from src.graph.link import Link
from src.graph.node import Node
from src.view.ViewApp import ViewApp

from PySide6.QtCore import QObject, QTimer, Signal

from src.parsing import MapParser
from src.parsing.errors.MapErrors import MapError
from src.parsing.models import MapModel
from src.simulation.drone import Drone


class ControllerError(Exception):
    """
    Exception raised for errors in the Controller.
    """

    def __init__(self, message: str):
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

    def __init__(self) -> None:
        """
        Initializes the Controller.

        Args:
            map_path (str): The path to the map configuration file.
        """
        super().__init__()
        self.logger = logging.getLogger("Fly-In")
        self.drone_list: list[Drone] = []
        self.graph: Graph = Graph()

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

        # content: str = self.__read_file()
        # map_model: MapModel = self.__parse_content(content)

        # self.__init_graph(map_model)

        # QTimer.singleShot(2000, lambda: self.__continue_process(map_model))

        sys.exit(self.app.app.exec())

    # def __continue_process(self, map_model: MapModel) -> None:
    #     self.logger.info("Drawing graph...")
    #     # self.app_window.draw_graph(self.graph)
    #     self.logger.info("Graph drawn successfully")

    #     self.__init_simulation(map_model.nb_drones, map_model.start_hub.pos)
    #     self.logger.info("Simulation prête")
    #     path, distance = Djikstra.dijkstra(self.graph)
    #     self.logger.info(f"le chemin est {path}")
    #     self.logger.info(distance)
    #     self.logger.info("Programm exit")

    def load_file(self, path: str):
        if path == "":
            return
        self.logger.info(f"File received: {path}")

        content = self.__read_file(path)
        if content != "":
            map_model = self.__parse_content(content)

        if map_model:
            self.__init_graph(map_model)
            self.logger.info("File successfully loaded")
        else:
            self.logger.info("File not loaded")

    def __read_file(self, path: str) -> str:
        """
        Reads the content of the map file.

        Returns:
            str: The plain text content of the map file.
        """
        self.logger.info(f"File to open and read: '{path}'")
        try:
            with open(path) as f:
                content: str = f.read()
            return content
        except (FileNotFoundError, PermissionError) as e:
            self.logger.error(f"File: {e}")
            self.file_error.emit(f"Error: {e}")
            return ""

    def __parse_content(self, content: str) -> MapModel | None:
        """
        Parses the model extracted from the file content.

        Args:
            content (str): Content string of the map file.

        Returns:
            MapModel: A parsed map model representing hubs and paths.
        """
        self.logger.info(content)
        try:
            parser: MapParser = MapParser(content)
            config = parser.process()
            return config
        except MapError as e:
            self.logger.error(f"{e}")
            self.file_error.emit(f"Error: {e}")
            return None

    def __init_graph(self, map_model: MapModel):
        # self.graph.name = self.map_path
        hubs = map_model.hubs.copy()
        hubs.append(map_model.end_hub)
        hubs.append(map_model.start_hub)
        for hub in hubs:
            node: Node = Node(
                hub.name,
                hub.hub_type.value,
                hub.pos,
                hub.zone.value,
                hub.color,
            )
            self.graph.add_node(node)

        for connection in map_model.connections:
            link: Link = Link(
                f"{connection.zone1}-{connection.zone2}",
                connection.max_link_capacity,
            )
            self.graph.nodes[connection.zone1].add_connected_node(
                self.graph.nodes[connection.zone2]
            )
            self.graph.nodes[connection.zone2].add_connected_node(
                self.graph.nodes[connection.zone1]
            )
            self.graph.add_link(link)

        self.logger.info(repr(self.graph))

    # def __init_simulation(
    #     self, nb_drone: int, start_pos: Tuple[int, int]
    # ) -> None:
    #     """
    #     Initializes the simulation by instantiating drones.

    #     Args:
    #         nb_drone (int): The number of drones to initialize.
    #         start_pos (Tuple[int, int]): Drone start coordinates (x, y).
    #     """
    #     for nb in range(nb_drone):
    #         self.drone_list.append(Drone(nb + 1, start_pos))
    #     self.logger.info("All drones initialized")

    def exit_program(self) -> None:
        """
        Safely halts execution and exits the program.

        Raises:
            ControllerError: To break execution explicitly.
        """
        self.logger.info("Programm exit")
        raise ControllerError("Programm exit")
