from enum import Enum


class ZoneEnum(Enum):
    """Enumeration of possible zone types."""
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class HubTypeEnum(Enum):
    """Enumeration of standard hub types."""
    START = "start_hub"
    END = "end_hub"
    HUB = "hub"
