import argparse


class PausingArgumentParser(argparse.ArgumentParser):
    """
    Custom argument parser that does not call ``sys.exit`` on error.

    Extends :class:`argparse.ArgumentParser` with ``exit_on_error=False``
    so that invalid arguments raise an exception instead of terminating
    the process, allowing the caller to handle errors gracefully.
    """

    def __init__(self, name: str, description: str, epilog: str) -> None:
        """
        Initializes the parser with program metadata and registers
        all known arguments.

        Args:
            name (str): Program name displayed in the help text.
            description (str): Short description of the program.
            epilog (str): Text shown at the bottom of the help page.
        """
        super().__init__(
            exit_on_error=False,
            prog=name,
            description=description,
            epilog=epilog,
        )
        self._add_arguments()

    def _add_arguments(self) -> None:
        """
        Registers all command-line arguments accepted by the application.

        Internal flags (``--child``, ``--gui``) are suppressed from the
        public help output as they are injected automatically at runtime.
        """
        self.add_argument(
            "--child", action="store_true", help=argparse.SUPPRESS
        )
        self.add_argument("--gui", action="store_true", help=argparse.SUPPRESS)
