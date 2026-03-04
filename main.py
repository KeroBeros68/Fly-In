import logging
import os
import subprocess
import sys

from logs import setup_logger
from utils import check_process


def main():
    logger = logging.getLogger("Fly-In")
    logger.info("Programm starting")
    check_process()
    print("Hello from fly-in-2!")
    input("\n\nPress Enter to exit...")


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
