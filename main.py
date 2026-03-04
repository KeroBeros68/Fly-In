import os
import subprocess
import sys

from utils import check_process


def main():
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
    main()
