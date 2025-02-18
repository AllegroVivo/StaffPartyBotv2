from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional

################################################################################

__all__ = ("XIVTime",)

################################################################################
@dataclass
class XIVTime:

    hour: int
    minute: int
    timezone: str
    next_day: bool

################################################################################
    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> Optional[XIVTime]:

        if data is None:
            return None

        return cls(
            hour=data.get("hour"),
            minute=data.get("minute"),
            timezone=data.get("timeZone"),
            next_day=data.get("nextDay")
        )

################################################################################
