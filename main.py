import os
import subprocess
import sys


from src import Controller
from src.utils.logger import setup_logger

TERMINAL: list[str] = ["gnome-terminal", "--"]
# TERMINAL_KONSOLE: list[str] = ["konsole", "-e"]


def main() -> None:
    controller = Controller(map_path=sys.argv[2])
    controller.process()


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
