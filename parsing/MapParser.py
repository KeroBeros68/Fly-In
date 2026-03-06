import logging
from typing import Any

from errors.MapErrors import (
    MapInvalidCoordinatesError,
    MapMissingHubError,
    MapNbDronesError,
)
from parsing.models import ConnectionModel, HubModel, MapModel
from parsing.utils.Enum import HubTypeEnum, ZoneEnum


logger = logging.getLogger("Fly-In")


class MapParser:
    @staticmethod
    def process(data: str) -> MapModel:
        clean_data: list[str] = MapParser._sanitize(data)
        logger.info(f"Data sanitized: {clean_data}")

        value: Any = clean_data.pop(0)[11::]
        try:
            nb_drones: int = int(value)
        except ValueError:
            raise MapNbDronesError(nb_drones=value)

        hubs: list[HubModel] = MapParser._parse_hubs(clean_data)
        start_hub: HubModel = next(
            h for h in hubs if h.hub_type == HubTypeEnum.START
        )
        end_hub: HubModel = next(
            h for h in hubs if h.hub_type == HubTypeEnum.END
        )
        hubs = [h for h in hubs if h.hub_type == HubTypeEnum.HUB]

        map: MapModel = MapModel(
            nb_drones=nb_drones,
            start_hub=start_hub,
            end_hub=end_hub,
            hubs=hubs,
            connections=[],
        )
        return map

    @staticmethod
    def _sanitize(data: str) -> list[str]:
        clean_data = [
            d for d in data.split("\n") if d.strip() and not d.startswith("#")
        ]
        return clean_data

    @staticmethod
    def _parse_metadata(raw: str) -> dict:
        """Parse '[key=value key=value ...]' → {'key': 'value', ...}"""
        raw = raw.strip().strip("[]")
        result = {}
        for pair in raw.split():
            key, _, value = pair.partition("=")
            result[key] = value
        return result

    @staticmethod
    def _parse_hub_line(line: str) -> HubModel:
        """
        Parse une ligne hub: 'start_hub: name x y [color=green max_drones=2]'
        """
        hub_type_str, _, rest = line.partition(": ")
        hub_type = HubTypeEnum(hub_type_str)

        if "[" in rest:
            coords_part, meta_part = rest.split("[", 1)
            metadata = MapParser._parse_metadata(meta_part)
        else:
            coords_part = rest
            metadata = {}

        parts = coords_part.split()
        name = parts[0]
        try:
            x, y = int(parts[1]), int(parts[2])
        except ValueError:
            raise MapInvalidCoordinatesError(name=name, x=parts[1], y=parts[2])

        color = metadata.get("color")
        try:
            max_drones = (
                int(metadata["max_drones"])
                if "max_drones" in metadata
                else 1
            )
        except ValueError:
            raise MapNbDronesError(f"Error in max drone for {parts[0]}")
        zone = ZoneEnum(metadata["zone"]) if "zone" in metadata else ZoneEnum.NORMAL

        return HubModel(
            name=name,
            hub_type=hub_type,
            pos=(x, y),
            color=color,
            max_drones=max_drones,
            zone=zone,
        )

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
