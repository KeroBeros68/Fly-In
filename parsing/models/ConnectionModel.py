from typing import Optional

from pydantic import BaseModel, Field


class ConnectionModel(BaseModel):
    zone1: str = Field(
        description="Name of the first hub endpoint of the connection"
    )
    zone2: str = Field(
        description=(
            "Name of the second hub endpoint of the connection "
            "(zone1-zone2 is bidirectional)"
        )
    )
    max_link_capacity: Optional[int] = Field(
        default=1,
        ge=1,
        description=(
            "Maximum number of link allowed to traverse this"
            " connection simultaneously (default: 1, must be > 0)"
        ),
    )
