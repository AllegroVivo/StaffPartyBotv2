from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Dict
from Enums import DataCenter, GameWorld, HousingZone

if TYPE_CHECKING:
    from Classes import Venue, XIVLocation
################################################################################

__all__ = ("VenueLocation", )

VL = TypeVar("VL", bound="VenueLocation")

################################################################################
class VenueLocation:

    __slots__ = (
        "_parent",
        "data_center",
        "world",
        "zone",
        "ward",
        "plot",
        "apartment",
        "room",
        "subdivision",
    )

################################################################################
    def __init__(self, parent: Venue, **kwargs) -> None:

        self._parent: Venue = parent

        self.data_center: Optional[DataCenter] = kwargs.get("data_center", None)
        self.world: Optional[GameWorld] = kwargs.get("world", None)
        self.zone: Optional[HousingZone] = kwargs.get("zone", None)
        self.ward: Optional[int] = kwargs.get("ward", None)
        self.plot: Optional[int] = kwargs.get("plot", None)
        self.subdivision: Optional[bool] = kwargs.get("subdivision", False)
        self.apartment: Optional[int] = kwargs.get("apartment", None)
        self.room: Optional[int] = kwargs.get("room", None)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "data_center": self.data_center.value if self.data_center else None,
            "world": self.world.value if self.world else None,
            "zone": self.zone.value if self.zone else None,
            "ward": self.ward,
            "plot": self.plot,
            "apartment": self.apartment,
            "room": self.room,
            "subdivision": self.subdivision
        }

################################################################################
    def update_from_xiv_venue(self, xiv_venue: XIVLocation) -> None:

        self.data_center = DataCenter.from_xiv(xiv_venue.data_center)
        self.world = GameWorld.from_xiv(xiv_venue.world)
        self.zone = HousingZone.from_xiv(xiv_venue.zone)
        self.ward = xiv_venue.ward
        self.plot = xiv_venue.plot
        self.apartment = xiv_venue.apartment
        self.room = xiv_venue.room
        self.subdivision = xiv_venue.subdivision

################################################################################
    def format(self) -> str:

        ret = ""

        if self.data_center:
            ret += f"{self.data_center.name}"
        if self.world:
            ret += f", {self.world.name}"
        if self.zone:
            ret += f", {self.zone.proper_name}"
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
            ret = "Not Set"

        return ret

################################################################################
