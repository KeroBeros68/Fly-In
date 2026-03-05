from pydantic import BaseModel, Field

from parsing.models.HubModel import HubModel
from parsing.models.ConnectionModel import ConnectionModel


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
