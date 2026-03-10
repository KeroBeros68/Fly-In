from pydantic import BaseModel, Field, model_validator

from ...errors.MapErrors import (
    MapDuplicateConnectionError,
    MapDuplicateHubError,
    MapInvalidConnectionError,
)
from .HubModel import HubModel
from .ConnectionModel import ConnectionModel


class MapModel(BaseModel):
    nb_drones: int = Field(
        ge=1,
        description="Total number of drones to route from start to end hub",
    )
    start_hub: HubModel = Field(
        description=(
            "Unique starting hub where all drones begin the simulation"
        ),
    )
    end_hub: HubModel = Field(
        description=(
            "Unique destination hub where all drones must be delivered"
        ),
    )
    hubs: list[HubModel] = Field(
        description="List of all intermediate hubs in the network"
    )
    connections: list[ConnectionModel] = Field(
        description=(
            "List of all bidirectional edges connecting hubs in the network"
        )
    )

    @model_validator(mode="after")
    def duplicate_hub(self) -> "MapModel":
        names = [h.name for h in self.hubs]
        names.append(self.start_hub.name)
        names.append(self.end_hub.name)
        if len(names) != len(set(names)):
            raise MapDuplicateHubError("duplicate hub name detected")
        return self

    @model_validator(mode="after")
    def invalid_hub_in_connection(self) -> "MapModel":
        hub_names = [h.name for h in self.hubs]
        hub_names.append(self.start_hub.name)
        hub_names.append(self.end_hub.name)
        connection_names = {
            name for h in self.connections for name in (h.zone1, h.zone2)
        }
        for name in connection_names:
            if name not in hub_names:
                raise MapInvalidConnectionError(name)
        return self

    @model_validator(mode="after")
    def mirror_connection(self) -> "MapModel":
        seen: set[frozenset[str]] = set()
        for h in self.connections:
            key = frozenset((h.zone1, h.zone2))
            if key in seen:
                raise MapDuplicateConnectionError(h.zone1, h.zone2)
            seen.add(key)
        return self

    def __repr__(self) -> str:
        res: str = f"nb_drone: {self.nb_drones}\n\n"
        res += repr(self.start_hub) + "\n"
        res += repr(self.end_hub) + "\n"
        for h in self.hubs:
            res += repr(h) + "\n"
        res += "\n"
        for c in self.connections:
            res += repr(c) + "\n"
        return res
