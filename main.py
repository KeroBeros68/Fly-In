import logging
import os
import subprocess
import sys
import time

from src.FileLoader import FileLoader
from src.GraphBuilder import GraphBuilder
from src.parsing.MapParser import MapParser
from src.simulation.PathfindingAlgorithm import PathfindingAlgorithm
from src.simulation.Simulation import Simulation
from src.utils.PausingArgumentParser import PausingArgumentParser
from src.utils.RunSecurity.RunSecurity import RunEnvironmentError, RunSecurity
from src.utils.logger import setup_logger

PROG_NAME: str = "Fly-In"
PROG_DESCRIPTION: str = (
    "Drone routing simulation system: routes a fleet of drones from a start "
    "hub to an end hub through a network of connected zones, minimising the "
    "total number of simulation turns while respecting all capacity and "
    "movement constraints."
)
PROG_HELP: str = "Text at the bottom of help"

TERMINAL: list[str] = ["gnome-terminal", "--"]
# TERMINAL: list[str] = ["konsole", "-e"]
ALGORITHM: str = "dijkstra"


def main() -> None:
    """
    Main entry point for the Fly-In application.

    Initializes the controller with the map path from the command
    line arguments and starts the processing loop.
    """
    logger = logging.getLogger(PROG_NAME)

    if "--gui" not in sys.argv:
        secure_env = RunSecurity()
        try:
            secure_env.check_process()
            print("\n[OK] Environment secure. Launching GUI...")
            time.sleep(0.2)
        except RunEnvironmentError as e:
            logger.error(f"{e}")
            logger.info("Programm exit")
            input("\n\nPress Enter to exit...")
            return
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            input("\n\nPress Enter to exit...")
            return

        gui_args = [sys.executable, sys.argv[0], "--gui"] + [
            a for a in sys.argv[1:] if a != "--child"
        ]
        subprocess.Popen(
            gui_args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        return

    try:
        from src.Controller import Controller, ControllerError

        controller = Controller(
            PausingArgumentParser(PROG_NAME, PROG_DESCRIPTION, PROG_HELP),
            FileLoader(),
            GraphBuilder(),
            MapParser(),
            PathfindingAlgorithm.create(ALGORITHM),
            Simulation(),
        )
        controller.process()

    except ControllerError:
        pass
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    if "--child" not in sys.argv and "--gui" not in sys.argv:
        args = [sys.executable, sys.argv[0], "--child"] + sys.argv[1:]
        subprocess.Popen(
            [TERMINAL[0], TERMINAL[1]] + args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        os._exit(0)
    setup_logger(PROG_NAME)
    main()
