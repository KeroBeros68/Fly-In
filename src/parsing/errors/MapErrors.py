class MapError(Exception):
    """Base error for all map parsing errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"[MapError] {self.message}"


class MapFileNotFoundError(MapError):
    """Raised when the map file does not exist."""

    def __init__(self, file_path: str) -> None:
        super().__init__(f"Map file not found: '{file_path}'")


class MapEmptyError(MapError):
    """Raised when the map file is empty or contains only comments."""

    def __init__(self) -> None:
        super().__init__("Map file is empty")


class MapNbDronesError(MapError):
    """
    Raised when the drone count line is missing or contains a non-integer.
    """

    def __init__(self, nb_drones: str) -> None:
        super().__init__(f"Wrong drone number: '{nb_drones}'")


class MapHubError(MapError):
    """
    Raised when a hub line fails validation (bad format or Pydantic error).
    """

    def __init__(self, hub: str) -> None:
        super().__init__(f"Hub validation error: '{hub}'")


class MapPrefixError(MapError):
    """Raised when a line starts with an unrecognised prefix."""

    def __init__(self, prefix: str) -> None:
        super().__init__(f"Invalid prefix: '{prefix}'")


class MapMissingHubError(MapError):
    """Raised when start_hub or end_hub is missing from the map."""

    def __init__(self, hub_type: str) -> None:
        super().__init__(f"Missing required hub: '{hub_type}'")


class MapDuplicateHubError(MapError):
    """Raised when two hubs share the same name."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Duplicate hub name: '{name}'")


class MapZoneHubError(MapError):
    """Raised when a hub specifies an unrecognised zone name."""

    def __init__(self, zone: str) -> None:
        super().__init__(f"Invalid hub zone name: '{zone}'")


class MapInvalidCoordinatesError(MapError):
    """Raised when a hub has invalid (non-numeric) coordinates."""

    def __init__(self, name: str, x: str, y: str) -> None:
        super().__init__(f"Hub '{name}' has invalid coordinates: ({x}, {y})")


class MapConnectionError(MapError):
    """Base error for all connection-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class MapDuplicateConnectionError(MapConnectionError):
    """Raised when a connection (or its mirror) is defined more than once."""

    def __init__(self, zone1: str, zone2: str) -> None:
        super().__init__(
            f"Connection '{zone1}-{zone2}' is defined more than once"
        )


class MapInvalidConnectionError(MapConnectionError):
    """Raised when a connection references a hub that does not exist."""

    def __init__(self, hub_name: str) -> None:
        super().__init__(f"Connection references unknown hub: '{hub_name}'")


class MapConnectionValidationError(MapConnectionError):
    """Raised when a connection fails Pydantic field validation."""

    def __init__(self, detail: str) -> None:
        super().__init__(f"Connection validation error: '{detail}'")
