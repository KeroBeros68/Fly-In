import logging

from pydantic import ValidationError

from errors.MapErrors import (
    MapConnectionError,
    MapHubError,
    MapInvalidCoordinatesError,
    MapMissingHubError,
    MapNbDronesError,
)
from parsing.models import ConnectionModel, HubModel, MapModel
from parsing.utils.Enum import HubTypeEnum, ZoneEnum


logger = logging.getLogger("Fly-In")


class MapParser:
    def __init__(self, raw_data: str) -> None:
        self.__raw_data: str = raw_data
        self.__clean_data: list[str] = []
        self.__map_model: MapModel | None = None

    def process(self) -> MapModel:
        self.__sanitize(self.__raw_data)
        logger.info(f"Data sanitized: {self.__clean_data}")
        self.__build_map()
        logger.info(repr(self.__map_model))
        assert self.__map_model is not None
        return self.__map_model

    def __sanitize(self, data: str) -> None:
        self.__clean_data = [
            d for d in data.split("\n") if d.strip() and not d.startswith("#")
        ]

    def __build_map(self) -> None:
        data = self.__clean_data
        value: str = data.pop(0)[11::]
        try:
            nb_drones: int = int(value)
        except ValueError:
            raise MapNbDronesError(nb_drones=value)

        hubs: list[HubModel] = MapParser._parse_hubs(data)
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
            connections=MapParser._parse_connections(data),
        )

    @staticmethod
    def _parse_metadata(raw: str) -> dict[str, str]:
        """Parse '[key=value key=value ...]' → {'key': 'value', ...}"""
        raw = raw.strip().strip("[]")
        result = {}
        for pair in raw.split():
            key, _, value = pair.partition("=")
            result[key] = value
        return result

    @staticmethod
    def _split_meta(rest: str) -> tuple[str, dict]:
        """Sépare la partie base et les métadonnées '[key=value ...]'"""
        if "[" in rest:
            base, meta_part = rest.split("[", 1)
            return base, MapParser._parse_metadata(meta_part)
        return rest, {}

    @staticmethod
    def _parse_hub_line(line: str) -> HubModel:
        """
        Parse une ligne hub: 'start_hub: name x y [color=green max_drones=2]'
        """
        hub_type_str, _, rest = line.partition(": ")
        hub_type = HubTypeEnum(hub_type_str)

        coords_part, metadata = MapParser._split_meta(rest)

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

    @staticmethod
    def _parse_hubs(data: list[str]) -> list[HubModel]:
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
        return [MapParser._parse_hub_line(line) for line in hub_lines]

    @staticmethod
    def _parse_connections(data: list[str]) -> list[ConnectionModel]:
        connection_lines = [d for d in data if d.startswith("connection: ")]
        return [
            MapParser._parse_connection_line(line) for line in connection_lines
        ]

    @staticmethod
    def _parse_connection_line(line: str) -> ConnectionModel:
        _, _, rest = line.partition(": ")

        connection, metadata = MapParser._split_meta(rest)

        parts = connection.split("-")
        max_link_capacity = metadata.get("max_link_capacity", 1)

        try:
            return ConnectionModel(
                zone1=parts[0],
                zone2=parts[1],
                max_link_capacity=max_link_capacity,
            )
        except ValidationError as e:
            raise MapConnectionError(str(e)) from e
