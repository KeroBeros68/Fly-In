import logging
import os
import subprocess
import sys
import time

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

    if "--gui" not in sys.argv:
        secure_env = RunSecurity()
        try:
            secure_env.check_process()
            print("\n[OK] Environment secure. Launching GUI...")
            time.sleep(
                0.2
            )
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

        args_without_gui = [a for a in sys.argv if a != "--gui"]
        map_path = args_without_gui[1] if len(args_without_gui) > 1 else ""

        controller = Controller(map_path=map_path)
        controller.process()

    except ControllerError:
        pass


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
    setup_logger("Fly-In")
    main()
