from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List, Optional, Type, Dict, Any

from discord import User, Embed, Interaction, Message

from Classes.Common import ManagedObject, LazyUser, LazyMessage
from Enums import RPLevel
from UI.Common import FroggeView
from .VenueLocation import VenueLocation
from .VenueHours import VenueHours
from .VenueURLs import VenueURLs
from Utilities import Utilities as U

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
        self._nsfw: bool = kwargs.get("nsfw", False)

        self._rp_level: Optional[RPLevel] = (
            RPLevel(kwargs["rp_level"])
            if kwargs["rp_level"] is not None
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
        self: V = cls(mgr, new_data["id"], **new_data)
        await self.update_from_xiv_venue(interaction, xiv_venue)

################################################################################
    @property
    def xiv_id(self) -> str:

        return self._xiv_id

################################################################################
    @property
    def name(self) -> str:

        return self._name

    @name.setter
    def name(self, value: str) -> None:

        self._name = value
        self.update()

################################################################################
    @property
    def description(self) -> List[str]:

        return self._description

    @description.setter
    def description(self, value: Optional[List[str]]) -> None:

        self._description = value or []
        self.update()

################################################################################
    @property
    def mare_id(self) -> Optional[str]:

        return self._mare_id

    @mare_id.setter
    def mare_id(self, value: Optional[str]) -> None:

        self._mare_id = value
        self.update()

################################################################################
    @property
    def mare_password(self) -> Optional[str]:

        return self._mare_pass

    @mare_password.setter
    def mare_password(self, value: Optional[str]) -> None:

        self._mare_pass = value
        self.update()

################################################################################
    @property
    def hiring(self) -> bool:

        return self._hiring

    @hiring.setter
    def hiring(self, value: bool) -> None:

        self._hiring = value
        self.update()

################################################################################
    @property
    def pending(self) -> bool:

        return self._pending

    @pending.setter
    def pending(self, value: bool) -> None:

        self._pending = value
        self.update()

################################################################################
    @property
    def nsfw(self) -> bool:

        return self._nsfw

    @nsfw.setter
    def nsfw(self, value: bool) -> None:

        self._nsfw = value
        self.update()

################################################################################
    @property
    def rp_level(self) -> Optional[RPLevel]:

        return self._rp_level

    @rp_level.setter
    def rp_level(self, value: Optional[RPLevel]) -> None:

        self._rp_level = value
        self.update()

################################################################################
    @property
    async def managers(self) -> List[User]:

        return [await u.get() for u in self._users]

################################################################################
    @property
    def positions(self) -> List:

        return self._positions

################################################################################
    @property
    async def muted_users(self) -> List[User]:

        return [await u.get() for u in self._mutes]

################################################################################
    @property
    def tags(self) -> List[str]:

        return self._tags

################################################################################
    @property
    async def post_message(self) -> Optional[Message]:

        return await self._post_msg.get()

    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:

        self._post_msg.set(value)

################################################################################
    @property
    def location(self) -> VenueLocation:

        return self._location

################################################################################
    @property
    def urls(self) -> VenueURLs:

        return self._urls

################################################################################
    def update(self) -> None:

        self.bot.db.update.venue(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "xiv_id": self._xiv_id,
            "name": self._name,
            "description": self._description,
            "mare_id": self._mare_id,
            "mare_password": self._mare_pass,
            "hiring": self._hiring,
            "nsfw": self._nsfw,
            "rp_level": self._rp_level.value if self._rp_level else None,
            "user_ids": [u.id for u in self._users],
            "position_ids": [p.id for p in self._positions],
            "mute_ids": [u.id for u in self._mutes],
            "tags": self._tags,
            "post_url": self._post_msg.id,
            **self._location.to_dict(),
            **self._urls.to_dict(),
        }

################################################################################
    async def status(self) -> Embed:

        pass

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        pass

################################################################################
    async def update_from_xiv_venue(self, interaction: Interaction, venue: Optional[XIVVenue] = None) -> None:

        if venue is None:
            results = [
                v for v in
                await self.bot.xiv_client.get_venues_by_manager(interaction.user.id)
                if v.name.lower() == self.name.lower()
            ]
            if not results:
                error = U.make_error(
                    title="Unable to Import Venue",
                    message=(
                        "An error occurred while attempting to import the venue.\n\n"

                        "Either there are no venues with you listed as a manager on "
                        "the XIV Venues API, **or** there is no venue that you manage "
                        "that has the name you provided."
                    ),
                    solution=(
                        "If you are not listed as a manager for any venues on the XIV "
                        "Venues API, you will need to contact them to have yourself "
                        "added as a manager.\n\n"

                        "If you are listed as a manager for a venue, but the venue "
                        "was not found, please ensure that you have entered the name "
                        "of the venue correctly."
                    )
                )
                await interaction.respond(embed=error, ephemeral=True)
                return
            venue = results[0]

        self._xiv_id = venue.id
        self._name: str = venue.name
        self._description: List[str] = venue.description.copy() if venue.description else []

        self._mare_id: Optional[str] = venue.mare_id
        self._mare_pass: Optional[str] = venue.mare_pass
        self._hiring: bool = venue.hiring

        self._location.update_from_xiv_venue(venue.location)
        self._urls.update_from_xiv_venue(venue)

        self._users = [
            LazyUser(self, user_id)
            for user_id in venue.managers
        ]

        for s in self._schedule:
            s.delete()
        self._schedule = [
            VenueHours.from_xiv_schedule(self, h)
            for h in venue.schedule
        ]

        self.update()

################################################################################
