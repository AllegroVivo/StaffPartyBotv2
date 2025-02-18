from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Type, TypeVar, Any, Dict
################################################################################

__all__ = ("XIVScheduleOverride",)

SO = TypeVar("SO", bound="XIVScheduleOverride")

################################################################################
@dataclass
class XIVScheduleOverride:

    open: bool
    start: datetime
    end: datetime
    now: bool

################################################################################
    @classmethod
    def from_data(cls: Type[SO], data: Dict[str, Any]) -> SO:

        return cls(
            open=data.get("open"),
            start=datetime.fromisoformat(data.get("start")),
            end=datetime.fromisoformat(data.get("end")),
            now=data.get("isNow")
        )

################################################################################
