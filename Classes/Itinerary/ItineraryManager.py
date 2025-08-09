from __future__ import annotations

from typing import TYPE_CHECKING, List, Dict

from Classes.Common import LazyMessage

from .VenueOpening import VenueOpening

if TYPE_CHECKING:
    from Classes import StaffPartyBot, Venue
################################################################################

__all__ = ("ItineraryManager", )

################################################################################
class ItineraryManager:

    __slots__ = (
        "_state",
        "_openings",
        "_post_msgs",
    )

################################################################################
    def __init__(self, state: StaffPartyBot) -> None:

        self._state: StaffPartyBot = state

        self._openings: Dict[Venue, List[VenueOpening]] = {}
        self._post_msgs: List[LazyMessage] = []

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._state

################################################################################
    async def venue_runner(self) -> None:

        for venue in self.bot.venue_manager.venues:
            if venue in self._openings:
                continue

            if venue.will_open_within(4):

################################################################################
