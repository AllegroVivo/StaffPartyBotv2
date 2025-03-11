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
    zone: str
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
            zone=data.get("zone"),
            ward=data.get("ward"),
            plot=data.get("plot"),
            apartment=data.get("apartment"),
            room=data.get("room"),
            subdivision=data.get("subdivision"),
            shard=data.get("shard"),
            override=data.get("override")
        )

################################################################################
    def format(self) -> str:

        ret = ""

        if self.data_center:
            ret += f"{self.data_center}"
        if self.world:
            ret += f", {self.world}"
        if self.zone:
            ret += f", {self.zone}"
        if self.ward:
            ret += f", Ward {self.ward}"
        if self.subdivision:
            ret += " (Sub)"
        if self.plot:
            ret += f", Plot {self.plot}"
        if self.apartment:
            ret += f", Apt. {self.apartment}"
        if self.room:
            ret += f", Room {self.room}"

        if not ret:
            ret = "Location Not Set"

        return ret

################################################################################
