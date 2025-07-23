from __future__ import annotations

import hashlib
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List, Type, TypeVar, Any, Dict
from urllib.parse import urlparse

from discord import Embed, EmbedField, PartialEmoji, SelectOption, Interaction, Thread, Message, Forbidden, ChannelType

from Classes.Common import Identifiable, LazyMessage
from Assets import BotEmojis
from Enums import LinkType
from Errors import InsufficientPermissions
from UI.Common import ConfirmCancelView, BasicTextModal, FroggeSelectView
from UI.Venues import SpecialEventStatusView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import SpecialEventManager, StaffPartyBot, Venue
################################################################################

__all__ = ("SpecialEvent", )

SE = TypeVar("SE", bound="SpecialEvent")

################################################################################
class SpecialEvent(Identifiable):

    __slots__ = (
        "_mgr",
        "_title",
        "_description",
        "_location",
        "_start",
        "_length",
        "_links",
        "_requirements",
        "_post_msg",
    )

################################################################################
    def __init__(self, mgr: SpecialEventManager, id: int, **kwargs) -> None:

        super().__init__(id)

        self._mgr: SpecialEventManager = mgr

        self._title: str = kwargs.get("title")
        self._description: Optional[str] = kwargs.get("description")
        self._location: Optional[str] = kwargs.get("location")
        self._start: Optional[str] = kwargs.get("start")
        self._length: Optional[str] = kwargs.get("length")
        self._links: List[str] = kwargs.get("links")
        self._requirements: Optional[str] = kwargs.get("requirements")
        self._post_msg: LazyMessage = LazyMessage(self, kwargs.get("post_url"))

################################################################################
    @classmethod
    def new(
        cls: Type[SE],
        mgr: SpecialEventManager,
        title: str,
        description: Optional[str],
        location: Optional[str],
        start: Optional[datetime],
        length: Optional[str],
        links: List[str],
        requirements: Optional[str]
    ) -> SE:

        new_data = mgr.bot.db.insert.special_event(
            venue_id=mgr.venue.id,
            title=title,
            description=description,
            location=location,
            start=start,
            length=length,
            links=links,
            requirements=requirements
        )
        return cls(mgr, **new_data)

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._mgr.bot

################################################################################
    @property
    def venue(self) -> Venue:

        return self._mgr.venue

################################################################################
    @property
    def title(self) -> str:

        return self._title

    @title.setter
    def title(self, value: str) -> None:

        self._title = value
        self.update()

################################################################################
    @property
    def description(self) -> Optional[str]:

        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:

        self._description = value
        self.update()

################################################################################
    @property
    def location(self) -> Optional[str]:

        return self._location

    @location.setter
    def location(self, value: Optional[str]) -> None:

        self._location = value
        self.update()

################################################################################
    @property
    def start(self) -> Optional[str]:

        return self._start

    @start.setter
    def start(self, value: Optional[str]) -> None:

        self._start = value
        self.update()

################################################################################
    @property
    def length(self) -> Optional[str]:

        return self._length

    @length.setter
    def length(self, value: Optional[str]) -> None:

        self._length = value
        self.update()

################################################################################
    @property
    def links(self) -> List[str]:

        return self._links

    @links.setter
    def links(self, value: List[str]) -> None:

        self._links = value
        self.update()

################################################################################
    @property
    def requirements(self) -> Optional[str]:

        return self._requirements

    @requirements.setter
    def requirements(self, value: Optional[str]) -> None:

        self._requirements = value
        self.update()

################################################################################
    @property
    async def post_message(self) -> Optional[Message]:

        return await self._post_msg.get()

    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:

        self._post_msg.set(value)

    @property
    def post_url(self) -> Optional[str]:

        return self._post_msg.url

################################################################################
    def status(self) -> Embed:

        return U.make_embed(
            title=f"Event Status for {self._title}",
            description=(
                f"**Event Description:**\n"
                f"{self._description or '`Not Set`'}\n\n"
                
                f"**Location:** `{self._location or '`Not Set`'}`\n\n"
                
                f"**Participant Requirements:**\n"
                f"{self._requirements or '`Not Set`'}\n"
            ),
            fields=[
                EmbedField(
                    name=f"__{BotEmojis.Clock} Start Time__",
                    value=self._start or '`Not Set`',
                    inline=True
                ),
                EmbedField(
                    name=f"__{BotEmojis.Watch} Duration__",
                    value=(
                        f"`{self._length}`"
                        if self._length is not None
                        else '`Not Set`'
                    ),
                    inline=True
                ),
                EmbedField(
                    name=f"__{BotEmojis.GenericLinkIcon} Links__",
                    value=self._links_field(),
                    inline=False
                )
            ]
        )

################################################################################
    def compile(self) -> Embed:

        return U.make_embed(
            title=self.title,
            description=(
                "**Event Description:**\n"
                f"{self._description or '`Not Set`'}\n\n"
                
                f"{U.draw_line(extra=30)}"
            ),
            fields=[
                EmbedField(
                    name=f"__{BotEmojis.World} Location__ {BotEmojis.World}",
                    value=self._location or '`Not Set`',
                    inline=False
                ),
                EmbedField(
                    name=f"__{BotEmojis.Clock} Start Time__",
                    value=self._start or '`Not Set`',
                    inline=True
                ),
                EmbedField(
                    name=f"__{BotEmojis.Watch} Duration__",
                    value=(
                        f"`{self._length}`"
                        if self._length is not None
                        else '`Not Set`'
                    ),
                    inline=True
                ),
                EmbedField(
                    name=f"__{BotEmojis.GenericLinkIcon} Links {BotEmojis.GenericLinkIcon}__",
                    value=self._links_field(),
                    inline=False
                ),
                EmbedField(
                    name=f"__{BotEmojis.Spaceship} Requirements to Participate {BotEmojis.Spaceship}__",
                    value=(
                        "**What do I need to do to be able to participate "
                        "in this event?**\n"
                        f"{self._requirements or '`Not Set`'}\n\n"
                    ),
                    inline=False
                ),
            ]
        )

################################################################################
    def _links_field(self) -> str:

        return "\n".join(self.links_list()) or "`Not Set`"

################################################################################
    async def menu(self, interaction: Interaction) -> None:

        embed = self.status()
        view = SpecialEventStatusView(interaction.user, self)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    def update(self) -> None:

        self.bot.db.update.special_event(self)

################################################################################
    async def delete(self) -> None:

        self.bot.db.delete.special_event(self.id)

        post_message = await self.post_message
        if post_message is not None:
            try:
                await post_message.channel.delete()
            except Exception:
                pass

        self._mgr._events.remove(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "title": self._title,
            "description": self._description,
            "location": self._location,
            "start": self._start,
            "length": self._length,
            "links": self._links,
            "requirements": self._requirements,
            "post_url": self._post_msg.url if self._post_msg else None
        }

################################################################################
    def summary_field(self) -> EmbedField:

        return EmbedField(
            name=f"__{self._title}__",
            value=(
                f"**Location:** `{self._location or '`Not Set`'}`\n"
                f"**Start Time:** "
                f"{self._start if self._start else '`Not Set`'}\n"
                f"**Duration:** "
                f"`{self._length}`"
                if self._length
                else '`Not Set`'
            ),
            inline=False
        )

################################################################################
    @staticmethod
    def get_emoji_for_link_type(link_type: LinkType) -> PartialEmoji:

        match link_type:
            case LinkType.Carrd:
                return BotEmojis.CarrdLogo
            case LinkType.Discord:
                return BotEmojis.DiscordLogo
            case LinkType.Facebook:
                return BotEmojis.FacebookLogo
            case LinkType.Instagram:
                return BotEmojis.InstagramLogo
            case LinkType.Bluesky:
                return BotEmojis.BlueskyLogo
            case LinkType.YouTube:
                return BotEmojis.YouTubeLogo
            case LinkType.TikTok:
                return BotEmojis.TikTokLogo
            case LinkType.Twitch:
                return BotEmojis.TwitchLogo
            case LinkType.Spotify:
                return BotEmojis.SpotifyLogo
            case LinkType.SoundCloud:
                return BotEmojis.SoundCloudLogo
            case LinkType.Schedule:
                return BotEmojis.CalendarLogo
            case _:
                return BotEmojis.GenericLinkIcon

################################################################################
    @staticmethod
    def extract_root_domain(url: str) -> str:
        """
        Parses 'url' to extract the host (netloc), remove 'www.' if present,
        and then try to isolate a 'root' domain (e.g. 'example' from 'sub.example.co.uk').
        Returns the final piece capitalized, or an empty string if no domain found.
        """

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url  # add default scheme for parsing

        parsed = urlparse(url)
        # netloc is the host: e.g. 'www.example.com' or 'sub.example.co.uk'
        netloc = parsed.netloc or ""

        # In case there's a user:pass@host format
        if '@' in netloc:
            netloc = netloc.split('@', 1)[-1]

        # Remove a leading 'www.'
        if netloc.startswith("www."):
            netloc = netloc[4:]

        # If there's nothing left, bail out
        if not netloc:
            return ""

        # Split on dots, e.g. 'sub.example.co.uk' => ['sub','example','co','uk']
        parts = netloc.split('.')

        # If there's only 1 part, e.g. 'localhost' or 'example',
        # just use that as domain.
        if len(parts) == 1:
            return parts[0].capitalize()

        # For 2 or more parts, the last part is TLD (like 'com' or 'co.uk')
        # The second to last part is likely the "root" domain.
        # e.g. parts = ['sub','example','co','uk'] => root domain is 'example'
        # e.g. parts = ['example','com'] => root domain is 'example'
        # We'll pick parts[-2].
        root = parts[-2]
        return root.capitalize()

################################################################################
    def links_list(self) -> List[str]:

        links = []
        for link in self._links:
            if not link.startswith(('http://', 'https://')):
                link = 'https://' + link  # add default scheme for parsing

            link_type = LinkType.identify_link_type(link)
            link_name = (
                link_type.proper_name
                if link_type != LinkType.Other
                else self.extract_root_domain(link)
            )
            links.append(f"{self.get_emoji_for_link_type(link_type)} [{link_name}]({link})")

        return links

################################################################################
    def select_option(self) -> SelectOption:

        return SelectOption(
            label=self._title,
            value=str(self.id)
        )

################################################################################
    async def remove(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Confirm Deletion",
            description=(
                f"Are you sure you want to delete the event "
                f"**{self._title}**?\n\n"
                
                f"This action cannot be undone."
            )
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        await self.delete()

################################################################################
    async def set_title(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Event Title",
            attribute="Title",
            example="eg. 'Staff Party 2025'",
            cur_val=self.title
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.title = modal.value
        await self.update_post_components()

################################################################################
    async def set_description(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Event Description",
            attribute="Description",
            example="eg. 'Join us for the party of the year!'",
            cur_val=self.description,
            max_length=500,
            multiline=True
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.description = modal.value
        await self.update_post_components()

################################################################################
    async def set_location(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Event Location",
            attribute="Location",
            example="eg. 'The Beach by Ur Mom's House'",
            max_length=150,
            cur_val=self.location
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.location = modal.value
        await self.update_post_components()

################################################################################
    async def set_start(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Event Start Time",
            attribute="Start Time",
            example="e.g. '2025-10-01 14:00 EST'",
            cur_val=self.start,
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.start = modal.value
        await self.update_post_components()

################################################################################
    async def set_length(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Event Length",
            attribute="Length",
            example="eg. '69 hours'",
            cur_val=self.length
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.length = modal.value
        await self.update_post_components()

################################################################################
    async def set_requirements(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Event Requirements",
            attribute="Requirements",
            example="eg. 'Must be frog-positive to attend'",
            max_length=1000,
            cur_val=self.requirements,
            multiline=True
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.requirements = modal.value
        await self.update_post_components()

################################################################################
    async def add_link(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Add Link",
            attribute="Link",
            example="eg. 'https://example.com'",
            max_length=200
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        if modal.value.lower() in self._links:
            return

        self._links.append(modal.value)
        self.update()

        await self.update_post_components()

################################################################################
    async def remove_link(self, interaction: Interaction) -> None:

        def short_hash_for_link(link: str, length: int = 8) -> str:
            """
            Returns a short string (up to 'length' hex digits)
            uniquely identifying the given link, using SHA256.
            """
            sha = hashlib.sha256(link.encode("utf-8")).hexdigest()
            return sha[:length]

        prompt = U.make_embed(
            title="Remove Link",
            description=(
                f"**[`{len(self._links)}`] Links Registered**\n\n"
                f"{self._links_field()}"
            ),
        )

        id_map = {}
        options = []
        for link in self._links:
            short_id = short_hash_for_link(link, length=8)
            id_map[short_id] = link
            label = U.string_clamp(link, 100)

            options.append(
                SelectOption(
                    label=label,
                    value=short_id,
                    emoji=self.get_emoji_for_link_type(LinkType.identify_link_type(link))
                )
            )

        view = FroggeSelectView(interaction.user, options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        real_link = id_map.get(view.value)
        if real_link and real_link in self._links:
            self._links.remove(real_link)

        self.update()
        await self.update_post_components()

################################################################################
    async def post(self, interaction: Interaction) -> None:

        await interaction.response.defer(invisible=False, ephemeral=True)

        post_channel = await self._mgr.post_channel
        if post_channel is None:
            error = U.make_error(
                title="Special Events Posting Channel Not Set",
                message="The special events posting channel has not been set for this server.",
                solution=(
                    "Please contact a server administrator to set the "
                    "special events channel."
                )
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        # Handling threads
        matching_thread = next((t for t in post_channel.threads if t.name.lower() == self.title.lower()), None)
        # applied_tags = await self.get_tags()
        if matching_thread:
            # Clear the matching thread
            # await matching_thread.edit(applied_tags=applied_tags)
            async for m in matching_thread.history():
                await m.delete()
            action = matching_thread.send  # type: ignore
        else:
            # Or create a new thread if no matching one
            action = lambda **kw: post_channel.create_thread(name=self.title, **kw)  # applied_tags=applied_tags, **kw)

        # Post or create thread and handle permissions error
        try:
            result = await action(embeds=[self.compile()])
            if isinstance(result, Thread):
                self.post_message = await result.fetch_message(result.last_message_id)
            else:
                self.post_message = result
        except Forbidden:
            error = InsufficientPermissions(post_channel, "Send Messages")
            await interaction.respond(embed=error, ephemeral=True)

################################################################################
    async def update_post_components(self) -> None:

        post_message = await self.post_message
        if post_message is None:
            return

        await post_message.edit(embed=self.status())

################################################################################