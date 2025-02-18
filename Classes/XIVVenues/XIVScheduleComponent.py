from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Type, TypeVar, Any, Dict

from .XIVTime import XIVTime
from .XIVTimeInterval import XIVTimeInterval
from .XIVTimeResolution import XIVTimeResolution
from .XIVUTCTime import XIVUTCTime
################################################################################

__all__ = ("XIVScheduleComponent",)

SC = TypeVar("SC", bound="XIVScheduleComponent")

################################################################################
@dataclass
class XIVScheduleComponent:

    commencing: Optional[Any]
    day: str
    start: XIVTime
    end: Optional[XIVTime]
    interval: XIVTimeInterval
    location: Optional[str]
    resolution: XIVTimeResolution
    utc: XIVUTCTime

################################################################################
    @classmethod
    def from_data(cls: Type[SC], data: Dict[str, Any]) -> SC:

        return cls(
            commencing=data.get("commencing"),
            day=data.get("day"),
            start=XIVTime.from_data(data.get("start")),
            end=XIVTime.from_data(data.get("end")),
            interval=XIVTimeInterval.from_data(data.get("interval")),
            location=data.get("location"),
            resolution=XIVTimeResolution.from_data(data.get("resolution")),
            utc=XIVUTCTime.from_data(data.get("utc"))
        )

################################################################################
