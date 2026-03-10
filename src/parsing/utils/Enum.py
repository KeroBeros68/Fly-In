from enum import Enum


class ZoneEnum(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class HubTypeEnum(Enum):
    START = "start_hub"
    END = "end_hub"
    HUB = "hub"
