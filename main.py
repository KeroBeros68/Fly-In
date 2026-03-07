import logging
import os
import subprocess
import sys

from errors.MapErrors import MapError
from logs import setup_logger
from parsing import MapParser
from utils import check_process

logger = logging.getLogger("Fly-In")


def exit_programm() -> None:
    logger.info("Programm exit")
    input("\n\nPress Enter to exit...")
    os._exit(0)


def main() -> None:
    logger.info("Programm starting")
    check_process()
    file: str = sys.argv[2]
    logger.info(f"File to open and read: '{file}'")
    try:
        with open(file) as f:
            content: str = f.read()
    except (FileNotFoundError, PermissionError) as e:
        logger.error(f"File: {e}")
        exit_programm()
    except IndexError:
        logger.error("Usage: python main.py <map_file>")
        exit_programm()

    logger.info(content)
    try:
        config = MapParser.process(content)
        logger.info(config)
    except MapError as e:
        logger.error(f"{e}")
        exit_programm()

    print(config.connections)
    exit_programm()


if __name__ == "__main__":
    if "--child" not in sys.argv:
        args = ["python3", sys.argv[0], "--child"] + sys.argv[1:]
        subprocess.Popen(
            ["gnome-terminal", "--"] + args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        os._exit(0)
    setup_logger()
    main()
