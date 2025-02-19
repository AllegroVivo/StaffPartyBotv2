from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List, Optional, Type

from discord import User, Embed, Interaction

from Classes.Common import ManagedObject, LazyUser, LazyMessage
from Enums import RPLevel
from UI.Common import FroggeView
from .VenueLocation import VenueLocation
from .VenueHours import VenueHours
from .VenueURLs import VenueURLs
from ..Common.FroggeObject import T

if TYPE_CHECKING:
    from Classes import VenueManager, XIVVenue
################################################################################

__all__ = ("Venue",)

V = TypeVar("V", bound="Venue")

################################################################################
class Venue(ManagedObject):

    __slots__ = (
        "_name",
        "_description",
        "_hiring",
        "_users",
        "_location",
        "_urls",
        "_pending",
        "_schedule",
        "_nsfw",
        "_tags",
        "_rp_level",
        "_positions",
        "_post_msg",
        "_mare_id",
        "_mare_pass",
        "_mutes",
        "_xiv_id",
    )

################################################################################
    def __init__(self, mgr: VenueManager, id: int, **kwargs):

        super().__init__(mgr, id)

        self._xiv_id: str = kwargs.pop("xiv_id")
        self._name: str = kwargs.pop("name")

        self._description: List[str] = kwargs.get("description", [])
        self._tags: List[str] = kwargs.get("tags", [])

        self._mare_id: Optional[str] = kwargs.get("mare_id")
        self._mare_pass: Optional[str] = kwargs.get("mare_password")

        self._hiring: bool = kwargs.get("hiring", True)
        self._pending: bool = kwargs.get("pending", True)
        self._nsfw: bool = kwargs.get("nsfw", False)

        self._rp_level: Optional[RPLevel] = (
            RPLevel(kwargs["rp_level"])
            if "rp_level" in kwargs
            else None
        )

        self._location: VenueLocation = VenueLocation(self, **kwargs)
        self._schedule: List[VenueHours] = [
            VenueHours(self, **sch)
            for sch in kwargs.get("schedules", [])
        ]
        self._positions = []

        self._users: List[LazyUser] = [
            LazyUser(self, user_id)
            for user_id in kwargs.get("user_ids", [])
        ]
        self._mutes: List[LazyUser] = [
            LazyUser(self, user_id)
            for user_id in kwargs.get("mute_ids", [])
        ]

        self._urls: VenueURLs = VenueURLs(self, **kwargs)
        self._post_msg: LazyMessage = LazyMessage(self, kwargs.get("post_url"))

################################################################################
    @classmethod
    async def new(cls: Type[V], mgr: VenueManager, xiv_venue: XIVVenue, interaction: Interaction) -> V:

        new_data = mgr.bot.db.insert.venue(xiv_venue.id, xiv_venue.name)

################################################################################
    async def status(self) -> Embed:

        pass

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        pass

################################################################################
