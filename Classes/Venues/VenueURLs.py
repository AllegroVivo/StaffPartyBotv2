from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Dict

from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import Venue, StaffPartyBot, XIVVenue
################################################################################

__all__ = ("VenueURLs",)

VD = TypeVar("VD", bound="VenueDetails")

################################################################################
class VenueURLs:

    __slots__ = (
        "_parent",
        "_logo_url",
        "_discord_url",
        "_website_url",
        "_banner_url",
        "_app_url",
    )

################################################################################
    def __init__(self,  parent: Venue, **kwargs) -> None:

        self._parent: Venue = parent

        self._discord_url: Optional[str] = kwargs.get("discord_url")
        self._website_url: Optional[str] = kwargs.get("website_url")
        self._logo_url: Optional[str] = kwargs.get("logo_url")
        self._banner_url: Optional[str] = kwargs.get("banner_url")
        self._app_url: Optional[str] = kwargs.get("app_url")

################################################################################
