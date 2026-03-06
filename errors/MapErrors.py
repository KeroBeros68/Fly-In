class MapError(Exception):
    """Base error for all map parsing errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"[MapError] {self.message}"


class MapFileNotFoundError(MapError):
    """Raised when the map file does not exist."""

    def __init__(self, file_path: str):
        super().__init__(f"Map file not found: '{file_path}'")


class MapNbDronesError(MapError):
    def __init__(self, nb_drones: str):
        super().__init__(f"Wrong drone number: '{nb_drones}'")


class MapMissingHubError(MapError):
    """Raised when start_hub or end_hub is missing from the map."""

    def __init__(self, hub_type: str):
        super().__init__(f"Missing required hub: '{hub_type}'")


class MapDuplicateHubError(MapError):
    """Raised when two hubs share the same name."""

    def __init__(self, name: str):
        super().__init__(f"Duplicate hub name: '{name}'")


class MapInvalidCoordinatesError(MapError):
    """Raised when a hub has invalid (non-numeric) coordinates."""

    def __init__(self, name: str, x: str, y: str):
        super().__init__(
            f"Hub '{name}' has invalid coordinates: ({x}, {y})"
        )
