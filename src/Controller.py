import logging
import os
from typing import NoReturn

from src.parsing import MapParser
from src.parsing.errors.MapErrors import MapError
from src.utils.check_env.env_check import RunEnvironmentError, RunSecurity


class Controller():
    def __init__(self, map_path: str) -> None:
        self.logger = logging.getLogger("Fly-In")
        self.map_path: str = map_path

    def process(self) -> None:
        self.logger.info("Programm starting")
        secure_check = RunSecurity()
        try:
            secure_check.check_process()
        except RunEnvironmentError as e:
            self.logger.error(f"{e}")
            self.exit_programm()

        content: str = self.__read_file()
        self.__parse_content(content)
        self.exit_programm()

    def __read_file(self) -> str:
        self.logger.info(f"File to open and read: '{self.map_path}'")
        try:
            with open(self.map_path) as f:
                content: str = f.read()
            return content
        except (FileNotFoundError, PermissionError) as e:
            self.logger.error(f"File: {e}")
            self.exit_programm()
        except IndexError:
            self.logger.error("Usage: python main.py <map_file>")
            self.exit_programm()

    def __parse_content(self, content: str) -> None:
        self.logger.info(content)
        try:
            parser: MapParser = MapParser(content)
            config = parser.process()
        except MapError as e:
            self.logger.error(f"{e}")
            self.exit_programm()
        print(repr(config))

    def exit_programm(self) -> NoReturn:
        self.logger.info("Programm exit")
        input("\n\nPress Enter to exit...")
        os._exit(0)
