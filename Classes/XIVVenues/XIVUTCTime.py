from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional

from .XIVTime import XIVTime
################################################################################

__all__ = ("XIVUTCTime",)

################################################################################
@dataclass
class XIVUTCTime:

    from_value: Optional[Any]
    day: int
    start: XIVTime
    end: XIVTime
    location: Optional[Any]

################################################################################
    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> XIVUTCTime:

        return cls(
            from_value=data.get("from"),
            day=data.get("day"),
            start=XIVTime.from_data(data.get("start")),
            end=XIVTime.from_data(data.get("end")) if data.get("end") else None,
            location=data.get("location")
        )

################################################################################
