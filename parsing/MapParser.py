
import logging
from typing import Any

from errors.MapErrors import MapNbDronesError
from parsing.models import MapModel


logger = logging.getLogger("Fly-In")


class MapParser():
    @staticmethod
    def process(data: str) -> MapModel:
        map: MapModel | None = None
        clean_data: list[str] = MapParser._sanitize(data)
        logger.info(f"Data sanitized: {clean_data}")

        value: Any = clean_data.pop(0)[11::]
        try:
            nb_drones: int = int(value)
        except ValueError:
            raise MapNbDronesError(nb_drones=value)
        logger.info(f"Nb drone: {nb_drones}")

        # TODO: parse data and build map
        # map = MapModel(
        #     nb_drones=...,
        #     start_hub=...,
        #     end_hub=...,
        #     hubs=[...],
        #     connections=[...]
        # )
        return map

    @staticmethod
    def _sanitize(data: str) -> list[str]:
        clean_data = [
            d for d in data.split("\n") if d.strip() and not d.startswith("#")
        ]
        return clean_data
