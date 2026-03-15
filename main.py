import logging
import os
import subprocess
import sys


from src.utils.check_env.RunSecurity import RunEnvironmentError, RunSecurity
from src.utils.logger import setup_logger

TERMINAL: list[str] = ["gnome-terminal", "--"]
# TERMINAL_KONSOLE: list[str] = ["konsole", "-e"]


def main() -> None:
    """
    Main entry point for the Fly-In application.

    Initializes the controller with the map path from the command
    line arguments and starts the processing loop.
    """
    logger = logging.getLogger("Fly-In")
    secure_env = RunSecurity()
    try:
        secure_env.check_process()
        from src.Controller import Controller, ControllerError
        controller = Controller(map_path=sys.argv[2])
        controller.process()
    except RunEnvironmentError as e:
        logger.error(f"{e}")
        logger.info("Programm exit")
        input("\n\nPress Enter to exit...")
    except ControllerError:
        pass


if __name__ == "__main__":
    if "--child" not in sys.argv:
        args = ["python3", sys.argv[0], "--child"] + sys.argv[1:]
        subprocess.Popen(
            [TERMINAL[0], TERMINAL[1]] + args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        os._exit(0)
    setup_logger("Fly-In")
    main()
