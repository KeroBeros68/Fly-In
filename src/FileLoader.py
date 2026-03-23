import logging


class FileLoader:
    def __init__(self) -> None:
        self.logger = logging.getLogger("Fly-In")

    def read_file(self, path: str) -> str:
        """
        Reads the content of the map file.

        Returns:
            str: The plain text content of the map file.
        """
        self.logger.info(f"File to open and read: '{path}'")
        try:
            with open(path) as f:
                content: str = f.read()
            return content
        except (FileNotFoundError, PermissionError) as e:
            self.logger.error(f"File: {e}")
            return f"File: {e}"
