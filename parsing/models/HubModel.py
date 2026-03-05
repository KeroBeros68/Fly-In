from typing import Optional

from pydantic import BaseModel, Field

from parsing.utils.Enum import HubTypeEnum, ZoneEnum


class HubModel(BaseModel):
    name: str = Field(
        description=(
            "Unique identifier of the hub (no dashes or spaces allowed)"
        )
    )
    hub_type: HubTypeEnum = Field(
        description=(
            "Role of the hub in the network: start_hub, end_hub,"
            " or regular hub"
        )
    )
    pos: tuple[int, int] = Field(
        description="2D coordinates (x, y) of the hub on the map"
    )
    color: Optional[str] = Field(
        default=None,
        description=(
            "Optional display color for terminal or graphical"
            " representation (any single-word string)"
        ),
    )
    max_drones: Optional[int] = Field(
        default=1,
        description=(
            "Maximum number of drones allowed to occupy this hub"
            " simultaneously (default: 1, must be > 0)"
        ),
    )
    zone: Optional[ZoneEnum] = Field(
        default=ZoneEnum.NORMAL,
        description=(
            "Zone type determining movement cost and accessibility: normal"
            " (1 turn), restricted (2 turns), priority (1 turn, preferred),"
            " blocked (inaccessible)"
        ),
    )
