import logging
from typing import NoReturn, Optional, Tuple

from src.parsing import MapParser
from src.parsing.errors.MapErrors import MapError
from src.parsing.models import MapModel
from src.simulation.drone import Drone
from src.utils.check_env.env_check import RunEnvironmentError, RunSecurity


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


class Controller:
    """
    Main controller for managing the map parsing and simulation.

    Attributes:
        map_path (str): Path to the map to process.
        drone_list (list): List of initialized drones.
    """
    def __init__(
        self, map_path: str, secure_env: Optional[RunSecurity] = None
    ) -> None:
        """
        Initializes the Controller.

        Args:
            map_path (str): The path to the map configuration file.
            secure_env (RunSecurity, optional): Security check environment.
        """
        self.__secure_env: Optional[RunSecurity] = secure_env
        self.logger = logging.getLogger("Fly-In")

        self.map_path: str = map_path
        self.drone_list: list[Drone] = []

    def process(self) -> None:
        """
        Executes the main controller flow.

        Reads the map file, parses its content, and initializes
        the simulation. Validates the secure environment if provided.
        """
        self.logger.info("Programm starting")
        if self.__secure_env:
            try:
                self.__secure_env.check_process()
            except RunEnvironmentError as e:
                self.logger.error(f"{e}")
                self.exit_program()

        content: str = self.__read_file()
        map_model: MapModel = self.__parse_content(content)
        self.__init_simulation(map_model.nb_drones, map_model.start_hub.pos)
        self.exit_program()

    def __read_file(self) -> str:
        """
        Reads the content of the map file.

        Returns:
            str: The plain text content of the map file.
        """
        self.logger.info(f"File to open and read: '{self.map_path}'")
        try:
            with open(self.map_path) as f:
                content: str = f.read()
            return content
        except (FileNotFoundError, PermissionError) as e:
            self.logger.error(f"File: {e}")
            self.exit_program()
        except IndexError:
            self.logger.error("Usage: python main.py <map_file>")
            self.exit_program()

    def __parse_content(self, content: str) -> MapModel:
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
        except MapError as e:
            self.logger.error(f"{e}")
            self.exit_program()
        return config

    def __init_simulation(
        self, nb_drone: int, start_pos: Tuple[int, int]
    ) -> None:
        """
        Initializes the simulation by instantiating drones.

        Args:
            nb_drone (int): The number of drones to initialize.
            start_pos (Tuple[int, int]): Drone start coordinates (x, y).
        """
        for nb in range(nb_drone):
            self.drone_list.append(Drone(nb + 1, start_pos))
        self.logger.info("All drones initialized")
        for d in self.drone_list:
            print(d)

    def exit_program(self) -> NoReturn:
        """
        Safely halts execution and exits the program.

        Raises:
            ControllerError: To break execution explicitly.
        """
        self.logger.info("Programm exit")
        input("\n\nPress Enter to exit...")
        raise ControllerError("Programm exit")
