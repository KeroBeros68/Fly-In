import logging
from typing import NoReturn, Optional, Tuple

from src.parsing import MapParser
from src.parsing.errors.MapErrors import MapError
from src.parsing.models import MapModel
from src.simulation.drone import Drone
from src.utils.check_env.env_check import RunEnvironmentError, RunSecurity


class ControllerError(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"[ControllerError] {self.message}"


class Controller:
    def __init__(
        self, map_path: str, secure_env: Optional[RunSecurity] = None
    ) -> None:
        self.__secure_env: Optional[RunSecurity] = secure_env
        self.logger = logging.getLogger("Fly-In")

        self.map_path: str = map_path
        self.drone_list: list[Drone] = []

    def process(self) -> None:
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
        for nb in range(nb_drone):
            self.drone_list.append(Drone(nb + 1, start_pos))
        self.logger.info("All drones initialized")
        for d in self.drone_list:
            print(d)

    def exit_program(self) -> NoReturn:
        self.logger.info("Programm exit")
        input("\n\nPress Enter to exit...")
        raise ControllerError("Programm exit")
