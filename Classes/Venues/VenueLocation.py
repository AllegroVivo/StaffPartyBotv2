from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar
from Enums import DataCenter, GameWorld, HousingZone

if TYPE_CHECKING:
    from Classes import Venue
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
