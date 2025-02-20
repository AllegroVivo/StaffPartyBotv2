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
        "_dc",
        "_world",
        "_zone",
        "_ward",
        "_plot",
        "_apartment",
        "_room",
        "_subdivision",
    )

################################################################################
    def __init__(self, parent: Venue, **kwargs) -> None:

        self._parent: Venue = parent

        self._dc: Optional[DataCenter] = kwargs.get("data_center", None)
        self._world: Optional[GameWorld] = kwargs.get("world", None)
        self._zone: Optional[HousingZone] = kwargs.get("zone", None)
        self._ward: Optional[int] = kwargs.get("ward", None)
        self._plot: Optional[int] = kwargs.get("plot", None)
        self._subdivision: Optional[bool] = kwargs.get("subdivision", False)
        self._apartment: Optional[int] = kwargs.get("apartment", None)
        self._room: Optional[int] = kwargs.get("room", None)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "data_center": self._dc.value if self._dc else None,
            "world": self._world.value if self._world else None,
            "zone": self._zone.value if self._zone else None,
            "ward": self._ward,
            "plot": self._plot,
            "apartment": self._apartment,
            "room": self._room,
            "subdivision": self._subdivision
        }

################################################################################
    def update_from_xiv_venue(self, xiv_venue: XIVLocation) -> None:

        self._dc = DataCenter.from_xiv(xiv_venue.data_center)
        self._world = GameWorld.from_xiv(xiv_venue.world)
        self._zone = HousingZone.from_xiv(xiv_venue.zone)
        self._ward = xiv_venue.ward
        self._plot = xiv_venue.plot
        self._apartment = xiv_venue.apartment
        self._room = xiv_venue.room
        self._subdivision = xiv_venue.subdivision

################################################################################
