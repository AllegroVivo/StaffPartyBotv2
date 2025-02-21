from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List, Optional, Type, Dict, Any

from discord import User, Embed, Interaction, Message, EmbedField, ForumChannel, ForumTag, NotFound, Colour

from Assets import BotEmojis, BotImages
from Classes.Common import ManagedObject, LazyUser, LazyMessage
from Enums import RPLevel
from UI.Common import FroggeView, FroggeSelectView
from UI.Venues import VenuePostingMuteView, VenueStatusView
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

        self._xiv_id: str = kwargs.get("xiv_id")
        self._name: str = kwargs.get("name")

        self._description: List[str] = kwargs.get("description", [])
        self._tags: List[str] = kwargs.get("tags", [])

        self._mare_id: Optional[str] = kwargs.get("mare_id")
        self._mare_pass: Optional[str] = kwargs.get("mare_password")

        self._hiring: bool = kwargs.get("hiring", True)
        self._nsfw: bool = kwargs.get("nsfw", False)

        self._rp_level: Optional[RPLevel] = (
            RPLevel(kwargs["rp_level"])
            if kwargs.get("rp_level") is not None
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
    async def new(cls: Type[V], mgr: VenueManager, xiv_venue: XIVVenue) -> V:

        new_data = mgr.bot.db.insert.venue(xiv_venue.id, xiv_venue.name)
        self: V = cls(mgr, new_data["id"])
        await self.update_from_xiv_venue(xiv_venue)
        return self

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

    @property
    def post_url(self) -> Optional[str]:

        return self._post_msg.id

################################################################################
    @property
    def schedule(self) -> List[VenueHours]:

        return sorted(self._schedule, key=lambda x: x._day.value)

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
    async def status(self, post: bool = False) -> Embed:

        auth_user_value = (
            ("\n".join([f"• {user.mention}" for user in await self.managers]))
            if self._users
            else "`No Managers Specified`"
        )
        hours_value = (
            "\n".join([f"- {h.format()}" for h in self.schedule])
        ) if self.schedule else "`No Schedule Provided`"

        misc_value = (
            f"__RP Level:__ `{self.rp_level.proper_name if self.rp_level else 'Not Set'}`\n"
            f"__NSFW:__ `{'~Yes~' if self.nsfw else 'No'}`\n"
            f"__Venue Tags:__\n"
        )
        if self.tags:
            tags_list = [f"`{t}`" for t in self.tags]
            tags_formatted = [', '.join(tags_list[i:i+3]) for i in range(0, len(tags_list), 3)]
            misc_value += '\n'.join(tags_formatted)
        else:
            misc_value += "`Not Set`"

        if self.hiring:
            if self.positions:
                positions_list = [f"`{pos.name}`" for pos in self.positions]
                positions_formatted = [
                    ', '.join(positions_list[i:i+5])
                    for i in range(0, len(positions_list), 5)
                ]
                pos_value = '\n'.join(positions_formatted)
            else:
                pos_value = "`No sponsored positions.`"
        else:
            pos_value = "`Not accepting applications at this time`"

        fields = [
            EmbedField(
                name="__Owners/Managers__",
                value=f"{auth_user_value}\n{U.draw_line(extra=15)}",
                inline=False,
            ),
            EmbedField(
                name="__Open Hours__",
                value=f"{hours_value}\n{U.draw_line(extra=15)}",
                inline=True,
            ),
            EmbedField(
                name="__Accepting Applications__",
                value=U.yes_no_emoji(self.hiring),
                inline=True,
            ),
            EmbedField(
                name="__Location__",
                value=f"`{self._location.format()}`\n{U.draw_line(extra=15)}",
                inline=False,
            ),
            self.urls.field(),
            EmbedField(
                name=f"{BotEmojis.Eyes} __Other Info__ {BotEmojis.Eyes}",
                value=misc_value,
                inline=True,
            ),
            EmbedField(
                name="__We Employ the Following Jobs__",
                value=f"{pos_value}\n{U.draw_line(extra=15)}",
                inline=False,
            )
        ]
        if post:
            fields.append(EmbedField(
                name="__Post Status__",
                value=(
                    f"{BotEmojis.ArrowRight}{BotEmojis.ArrowRight}{BotEmojis.ArrowRight} "
                    f"[Click to View]({self.post_url}) "
                    f"{BotEmojis.ArrowLeft}{BotEmojis.ArrowLeft}{BotEmojis.ArrowLeft}\n"
                    if await self.post_message else f"{BotEmojis.Cross}  `Not Posted`\n"
                ),
                inline=False,
            ))

        return U.make_embed(
            title=f"Venue Profile: `{self.name}`",
            description=(
                (
                    "\n\n".join(self.description) if self.description
                    else "`No description provided.`"
                )
                + f"\n{U.draw_line(extra=33)}"
            ),
            thumbnail_url=self.urls.logo,
            fields=fields
        )

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        return VenueStatusView(user, self)

################################################################################
    async def update_from_xiv_venue(self, venue: Optional[XIVVenue] = None) -> None:

        if venue is None:
            venue = self.bot.xiv_client.get_venue_by_id(self._xiv_id)
            if venue is None:
                return

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
        await self.update_post_components(True, True)

################################################################################
    def complete(self, rp_bypass: bool = False) -> bool:

        if rp_bypass:
            return self._name is not None

        return all([
            self._name is not None,
            self.rp_level is not None,
        ])

################################################################################
    async def thread_tags(self) -> List[ForumTag]:

        return [
            t for t in (await self.manager.post_channel).available_tags
            if t.name.lower() in
            [t.lower() for t in self.tags]
        ][:5]

################################################################################
    async def post(
        self,
        interaction: Optional[Interaction],
        channel: ForumChannel,
        rp_bypass: bool = False
    ) -> None:

        if channel is None:
            if interaction is not None:
                error = U.make_error(
                    title="Venue Posting Channel Not Set",
                    message="The venue posting channel hasn't been set yet.",
                    solution="Contact a bot administrator to set it."
                )
                await interaction.respond(embed=error, ephemeral=True)
            return

        if not self.complete(rp_bypass):
            if interaction is not None:
                error = U.make_error(
                    title="Unable to Post Venue Profile",
                    message="The venue profile is not complete.",
                    solution="Please fully complete the venue profile before posting."
                )
                await interaction.respond(embed=error, ephemeral=True)
            return

        # Prepare the persistent view
        view = VenuePostingMuteView(self)
        self.bot.add_view(view)

        post_message = await self.post_message

        # If there's a thread with a matching name, update it and clear bot messages if post_msg is None
        thread = next((t for t in channel.threads if t.name.lower() == self.name.lower()), None)
        if thread is not None:
            await thread.edit(name=self.name, applied_tags=await self.thread_tags())
            # If post_msg is None, assume we might need to clear old messages from the bot
            if post_message is None:
                async for msg in thread.history():
                    if msg.author == self.bot.user:
                        await msg.delete()

        # Attempt to edit the existing message if it exists
        # Otherwise, create or post as necessary
        if post_message is not None:
            try:
                await post_message.edit(embed=await self.status(post=True), view=view)
            except NotFound:
                self.post_message = None  # Reset if the message was not found
        else:
            if not thread:
                # If no existing thread, create a new one
                thread = await channel.create_thread(
                    name=self.name, embed=await self.status(post=True),
                    applied_tags=self.thread_tags, view=view
                )
            # Grab the message we just posted
            try:
                self.post_message = await thread.fetch_message(thread.last_message_id)
            except NotFound:
                self.post_message = None

        self.update()

        if interaction is not None:
            await interaction.respond(embed=self.success_message(), ephemeral=True)

################################################################################
    def success_message(self) -> Embed:

        return U.make_embed(
            color=Colour.brand_green(),
            title="Profile Posted!",
            description=(
                "Hey, good job, you did it! Your venue profile was posted successfully!\n"
                f"{U.draw_line(extra=37)}\n"
                f"(__Venue Name:__ ***{self.name}***)\n\n"

                f"{BotEmojis.ArrowRight}  [Check It Out HERE!]"
                f"({self.post_url})  {BotEmojis.ArrowLeft}\n"
                f"{U.draw_line(extra=16)}"
            ),
            thumbnail_url=BotImages.ThumbsUpFrog,
            timestamp=True
        )

################################################################################
    async def update_post_components(self, status: bool, view: bool = True) -> None:

        post_message = await self.post_message
        if post_message is None:
            return

        if status and not view:
            await post_message.edit(embed=await self.status(post=True))
            return

        view = VenuePostingMuteView(self)
        self.bot.add_view(view)

        if view and not status:
            await post_message.edit(view=view)
        else:
            await post_message.edit(embed=await self.status(post=True), view=view)

################################################################################
    async def set_rp_level(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Set RP Level",
            description=(
                "Please select the RP level for your venue\n"
                "from the selector below."
            )
        )
        view = FroggeSelectView(interaction.user, RPLevel.select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.rp_level = RPLevel(int(view.value))

################################################################################
    async def toggle_hiring(self, interaction: Interaction) -> None:

        self.hiring = not self.hiring
        await interaction.edit()

################################################################################
    async def set_logo(self, interaction: Interaction) -> None:

        await self._urls.set_logo(interaction)

################################################################################
    async def set_application_url(self, interaction: Interaction) -> None:

        await self._urls.set_application_url(interaction)

################################################################################
    async def set_positions(self, interaction: Interaction) -> None:

        raise NotImplementedError

################################################################################
