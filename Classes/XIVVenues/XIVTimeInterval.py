from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
################################################################################

__all__ = ("XIVTimeInterval",)

################################################################################
@dataclass
class XIVTimeInterval:

    interval_type: int
    arg: int

################################################################################
    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> XIVTimeInterval:

        return cls(
            interval_type=data.get("intervalType"),
            arg=data.get("intervalArgument")
        )

################################################################################
