from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Any, Type, TypeVar, Dict
################################################################################

__all__ = ("XIVLocation",)

L = TypeVar("L", bound="XIVLocation")

################################################################################
@dataclass
class XIVLocation:

    data_center: str
    world: str
    district: str
    ward: int
    plot: int
    apartment: int
    room: int
    subdivision: bool
    shard: Optional[int]
    override: Optional[Any]

################################################################################
    @classmethod
    def from_data(cls: Type[L], data: Dict[str, Any]) -> L:

        return cls(
            data_center=data.get("dataCenter"),
            world=data.get("world"),
            district=data.get("district"),
            ward=data.get("ward"),
            plot=data.get("plot"),
            apartment=data.get("apartment"),
            room=data.get("room"),
            subdivision=data.get("subdivision"),
            shard=data.get("shard"),
            override=data.get("override")
        )

################################################################################
