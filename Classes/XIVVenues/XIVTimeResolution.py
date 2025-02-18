from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
################################################################################

__all__ = ("XIVTimeResolution",)

################################################################################
@dataclass
class XIVTimeResolution:

    start: datetime
    end: datetime
    now: bool
    in_week: bool

################################################################################
    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> Optional[XIVTimeResolution]:

        if data is None:
            return None

        return cls(
            start=datetime.fromisoformat(data.get("start")),
            end=datetime.fromisoformat(data.get("end")),
            now=data.get("isNow"),
            in_week=data.get("isWithinWeek")
        )

################################################################################
