from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from Enums import DataCenter, OpeningStatus, OpeningTag, Weekday

if TYPE_CHECKING:
    from Classes import ItineraryManager, Venue, StaffPartyBot
################################################################################

__all__ = ("VenueOpening",)

################################################################################
class VenueOpening:

    __slots__ = (
        "_id",
        "_mgr",
        "_venue_id",
        "_dc",
        "_open_dt",
        "_close_dt",
        "_status",
        "_will_open",
        "_address_override",
        "_is_collab",
        "_theme",
        "_primary_tag",
        "_responded_owner_id",
        "_responded_at",
    )

################################################################################
    def __init__(self, mgr: ItineraryManager, id: int, venue_id: int) -> None:

        self._id = id
        self._mgr: ItineraryManager = mgr
        self._venue_id: int = venue_id

        self._dc: DataCenter = None  # type: ignore  - will populate at the end
        self._open_dt: datetime = None  # type: ignore  - will populate at the end
        self._close_dt: datetime = None  # type: ignore  - will populate at the end

        # VOM-provided information
        self._status: OpeningStatus = OpeningStatus.Pending
        self._will_open: Optional[bool] = None
        self._address_override: Optional[str] = None
        self._is_collab: bool = False
        self._theme: Optional[str] = None
        self._primary_tag: Optional[OpeningTag] = None

        self._responded_owner_id: Optional[int] = None
        self._responded_at: Optional[datetime] = None

        self._get_venue_info()

################################################################################
    def _get_venue_info(self) -> None:

        # Populate the DataCenter and open/close times from the venue
        pass

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._mgr.bot

################################################################################
    @property
    def id(self) -> int:

        return self._id

################################################################################
    @property
    def mgr(self) -> ItineraryManager:

        return self._mgr

################################################################################
    @property
    def venue(self) -> Venue:

        return self.bot.venue_manager[self._venue_id]

################################################################################
