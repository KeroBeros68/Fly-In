import logging

from pydantic import ValidationError

from .errors.MapErrors import (
    MapConnectionValidationError,
    MapHubError,
    MapInvalidCoordinatesError,
    MapMissingHubError,
    MapNbDronesError,
    MapEmptyError,
)
from .models import ConnectionModel, HubModel, MapModel
from .utils.Enum import HubTypeEnum, ZoneEnum


logger = logging.getLogger("Fly-In")


class MapParser:
    """Parses a raw map file into a MapModel instance.

    The parser processes the raw text content of a map file,
    extracts hubs, connections, and metadata, and returns a
    fully validated MapModel object.
    """

    def __init__(self, raw_data: str) -> None:
        """Initialize the parser with the raw string content of a map file."""
        self.__raw_data: str = raw_data
        self.__clean_data: list[str] = []
        self.__map_model: MapModel | None = None

    def process(self) -> MapModel:
        """Parse the raw map data and return a validated MapModel.

        Sanitizes the input, extracts drone count, hubs and connections,
        then assembles and returns the complete MapModel.

        Returns:
            MapModel: The fully parsed and validated map.

        Raises:
            MapNbDronesError: If the drone count is missing or invalid.
            MapMissingHubError: If start_hub or end_hub is absent.
            MapInvalidCoordinatesError: If a hub has non-numeric coordinates.
            MapHubError: If a hub fails Pydantic validation.
            MapConnectionError: If a connection fails Pydantic validation.
        """
        self.__sanitize(self.__raw_data)
        logger.info(f"Data sanitized: {self.__clean_data}")
        self.__build_map()
        logger.info(repr(self.__map_model))
        assert self.__map_model is not None
        return self.__map_model

    def __sanitize(self, data: str) -> None:
        """Strip blank lines and comments from the raw input.

        Populates __clean_data with non-empty, non-comment lines.
        """
        self.__clean_data = [
            d for d in data.split("\n") if d.strip() and not d.startswith("#")
        ]
        if len(self.__clean_data) == 0:
            raise MapEmptyError()

    def __build_map(self) -> None:
        """Build the MapModel from the sanitized lines.

        Extracts the drone count from the first line, parses all hubs
        and connections, and stores the result in __map_model.
        """
        data = self.__clean_data.copy()
        if "nb_drones: " not in data[0]:
            raise MapNbDronesError("1st line must be 'nb_drone: XX'")

        value: str = data.pop(0)[11::]
        try:
            nb_drones: int = int(value)
        except ValueError:
            raise MapNbDronesError(nb_drones=value)

        hubs: list[HubModel] = self.__parse_hubs(data)
        start_hub: HubModel = next(
            h for h in hubs if h.hub_type == HubTypeEnum.START
        )
        end_hub: HubModel = next(
            h for h in hubs if h.hub_type == HubTypeEnum.END
        )
        hubs = [h for h in hubs if h.hub_type == HubTypeEnum.HUB]

        self.__map_model = MapModel(
            nb_drones=nb_drones,
            start_hub=start_hub,
            end_hub=end_hub,
            hubs=hubs,
            connections=self.__parse_connections(data),
        )

    def __parse_metadata(self, raw: str) -> dict[str, str]:
        """Parse a metadata block '[key=value ...]' into a dictionary.

        Args:
            raw: Raw metadata string including brackets.

        Returns:
            A dict mapping each key to its string value.
        """
        raw = raw.strip().strip("[]")
        result = {}
        for pair in raw.split():
            key, _, value = pair.partition("=")
            result[key] = value
        return result

    def __split_meta(self, rest: str) -> tuple[str, dict[str, str]]:
        """Split a line into its base content and optional metadata block.

        Args:
            rest: Remaining line content after the prefix (e.g. 'name x y
                                                                [key=val]').

        Returns:
            A tuple of (base_string, metadata_dict). If no '[' is present,
            metadata_dict is empty.
        """
        if "[" in rest:
            base, meta_part = rest.split("[", 1)
            return base, self.__parse_metadata(meta_part)
        return rest, {}

    def __parse_hub_line(self, line: str) -> HubModel:
        """Parse a single hub line into a HubModel.

        Expected format: '<type>: <name> <x> <y> [color=... max_drones=...
                                                                zone=...]'

        Args:
            line: A raw hub line from the map file.

        Returns:
            A validated HubModel instance.

        Raises:
            MapInvalidCoordinatesError: If x or y are non-numeric.
            MapNbDronesError: If max_drones is non-numeric.
            MapHubError: If Pydantic validation fails.
        """
        hub_type_str, _, rest = line.partition(": ")
        hub_type = HubTypeEnum(hub_type_str)

        coords_part, metadata = self.__split_meta(rest)

        parts = coords_part.split()
        name = parts[0]
        try:
            x, y = int(parts[1]), int(parts[2])
        except ValueError:
            raise MapInvalidCoordinatesError(name=name, x=parts[1], y=parts[2])

        color = metadata.get("color")
        try:
            max_drones = (
                int(metadata["max_drones"]) if "max_drones" in metadata else 1
            )
        except ValueError:
            raise MapNbDronesError(f"Error in max drone for {parts[0]}")
        zone = (
            ZoneEnum(metadata["zone"])
            if "zone" in metadata
            else ZoneEnum.NORMAL
        )
        try:
            return HubModel(
                name=name,
                hub_type=hub_type,
                pos=(x, y),
                color=color,
                max_drones=max_drones,
                zone=zone,
            )
        except ValidationError as e:
            raise MapHubError(str(e)) from e

    def __parse_hubs(self, data: list[str]) -> list[HubModel]:
        """Parse all hub lines from the sanitized data.

        Args:
            data: Sanitized lines from the map file.

        Returns:
            A list of HubModel instances (start, end, and intermediate hubs).

        Raises:
            MapMissingHubError: If start_hub or end_hub is absent.
        """
        if not any(d.startswith("start_hub: ") for d in data):
            raise MapMissingHubError("start_hub")
        if not any(d.startswith("end_hub: ") for d in data):
            raise MapMissingHubError("end_hub")

        hub_lines = [
            d
            for d in data
            if d.startswith("hub: ")
            or d.startswith("start_hub: ")
            or d.startswith("end_hub: ")
        ]
        return [self.__parse_hub_line(line) for line in hub_lines]

    def __parse_connections(self, data: list[str]) -> list[ConnectionModel]:
        """Parse all connection lines from the sanitized data.

        Args:
            data: Sanitized lines from the map file.

        Returns:
            A list of ConnectionModel instances.
        """
        connection_lines = [d for d in data if d.startswith("connection: ")]
        return [
            self.__parse_connection_line(line) for line in connection_lines
        ]

    def __parse_connection_line(self, line: str) -> ConnectionModel:
        """Parse a single connection line into a ConnectionModel.

        Expected format: 'connection: <zone1>-<zone2> [max_link_capacity=N]'

        Args:
            line: A raw connection line from the map file.

        Returns:
            A validated ConnectionModel instance.

        Raises:
            MapConnectionError: If Pydantic validation fails.
        """
        _, _, rest = line.partition(": ")

        connection, metadata = self.__split_meta(rest)

        parts = connection.split("-")
        max_link_capacity = metadata.get("max_link_capacity", 1)

        try:
            return ConnectionModel(
                zone1=parts[0],
                zone2=parts[1],
                max_link_capacity=int(max_link_capacity),
            )
        except ValidationError as e:
            raise MapConnectionValidationError(str(e)) from e
        except ValueError as e:
            raise MapConnectionValidationError(str(e))
