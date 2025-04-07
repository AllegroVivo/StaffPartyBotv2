from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import TYPE_CHECKING, Type, TypeVar, Optional, List, Dict, Any, Tuple

from discord import User, Embed, EmbedField, Interaction, Thread, Forbidden, Message, ForumTag, HTTPException, NotFound

from Assets import BotEmojis, BotImages
from Classes.Common import ManagedObject, LazyUser, LazyMessage
from Errors import InsufficientPermissions
from UI.DJs import DJProfileStatusView
from .DJAvailability import DJAvailability
from Enums import MusicGenre, Timezone, Weekday, Hours, XIVRegion
from Utilities import Utilities as U, FroggeColor
from UI.Common import AccentColorModal, BasicTextModal, FroggeSelectView, TimeSelectView, ConfirmCancelView
from .DJLinkManager import DJLinkManager
from .DJImageManager import DJImageManager

if TYPE_CHECKING:
    from Classes import DJManager
    from UI.Common import FroggeView
################################################################################

__all__ = ("DJProfile",)

DJP = TypeVar("DJP", bound="DJProfile")

################################################################################
class DJProfile(ManagedObject):

    __slots__ = (
        "_user",
        "_color",
        "_name",
        "_availability",
        "_nsfw",
        "_images",
        "_genres",
        "_aboutme",
        "_links",
        "_rates",
        "_tz",
        "_dm_pref",
        "_post_message",
        "_regions",
    )

################################################################################
    def __init__(self, mgr: DJManager, **kwargs) -> None:

        user_id = kwargs.pop("user_id")
        super().__init__(mgr, user_id)

        self._user: LazyUser = LazyUser(self,user_id)

        self._color: Optional[FroggeColor] = (
            FroggeColor(kwargs.get("color"))
            if kwargs.get("color")
            else None
        )
        self._name: Optional[str] = kwargs.get("name")
        self._nsfw: bool = kwargs.get("nsfw", False)
        self._genres: List[MusicGenre] = [MusicGenre(genre) for genre in kwargs.get("genres", [])]
        self._aboutme: Optional[str] = kwargs.get("aboutme")
        self._rates: Optional[str] = kwargs.get("rates")
        self._links: DJLinkManager = DJLinkManager(self, kwargs.get("links", []))
        self._images: DJImageManager = DJImageManager(self, **kwargs)
        self._availability: List[DJAvailability] = [
            DJAvailability(self, **availability)
            for availability
            in kwargs.get("availability", [])
        ]
        raw_tz = kwargs.get("timezone")
        self._tz: Optional[ZoneInfo] = ZoneInfo(raw_tz) if raw_tz else None
        self._dm_pref: bool = kwargs.get("dm_pref", True)
        self._post_message: LazyMessage = LazyMessage(self, kwargs.get("post_url"))
        self._regions: List[XIVRegion] = [XIVRegion(region) for region in kwargs.get("regions", [])]

################################################################################
    @classmethod
    def new(cls: Type[DJP], mgr: DJManager, user_id: int) -> DJP:

        new_data = mgr.bot.db.insert.dj_profile(user_id=user_id)
        return cls(mgr, **new_data)

################################################################################
    @property
    async def user(self) -> User:

        return await self._user.get()

################################################################################
    @property
    def color(self) -> Optional[FroggeColor]:

        return self._color

    @color.setter
    def color(self, value: FroggeColor) -> None:

        self._color = value
        self.update()

################################################################################
    @property
    def name(self) -> Optional[str]:

        return self._name

    @name.setter
    def name(self, value: str) -> None:

        self._name = value
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
    def genres(self) -> List[MusicGenre]:

        return self._genres

    @genres.setter
    def genres(self, value: List[MusicGenre]) -> None:

        self._genres = value
        self.update()

################################################################################
    @property
    def aboutme(self) -> Optional[str]:

        return self._aboutme

    @aboutme.setter
    def aboutme(self, value: Optional[str]) -> None:

        self._aboutme = value
        self.update()

################################################################################
    @property
    def rates(self) -> Optional[str]:

        return self._rates

    @rates.setter
    def rates(self, value: Optional[str]) -> None:

        self._rates = value
        self.update()

################################################################################
    @property
    def regions(self) -> List[XIVRegion]:

        return self._regions

    @regions.setter
    def regions(self, value: List[XIVRegion]) -> None:

        self._regions = value
        self.update()

################################################################################
    @property
    def links(self) -> DJLinkManager:

        return self._links

################################################################################
    @property
    def images(self) -> DJImageManager:

        return self._images

################################################################################
    @property
    def availability(self) -> List[DJAvailability]:

        return self._availability

    @availability.setter
    def availability(self, value: List[DJAvailability]) -> None:

        self._availability = value
        self.update()

################################################################################
    @property
    def timezone(self) -> Optional[ZoneInfo]:

        return self._tz

    @timezone.setter
    def timezone(self, value: ZoneInfo) -> None:

        self._tz = value
        self.update()

################################################################################
    @property
    def dm_pref(self) -> bool:

        return self._dm_pref

    @dm_pref.setter
    def dm_pref(self, value: bool) -> None:

        self._dm_pref = value
        self.update()

################################################################################
    @property
    async def post_message(self) -> Optional[Message]:

        return await self._post_message.get()

    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:

        self._post_message.set(value)

    @property
    def post_url(self) -> Optional[str]:

        return self._post_message.id

################################################################################
    def update(self) -> None:

        self.bot.db.update.dj_profile(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "color": self._color.value if self._color else None,
            "name": self._name,
            "nsfw": self._nsfw,
            "genres": [genre.value for genre in self._genres],
            "aboutme": self._aboutme,
            "rates": self._rates,
            "links": self._links._links,
            "logo_url": self._images._logo,
            "image_url": self._images._banner,
            "timezone": self._tz.key if self._tz else None,
            "dm_pref": self._dm_pref,
            "post_url": self._post_message.id,
            "regions": [region.value for region in self._regions],
        }

################################################################################
    async def status(self) -> Embed:

        dm_text = f"{U.yes_no_emoji(self._dm_pref)} "
        if self._dm_pref:
            dm_text += (
                f"**Accepting staffing-oriented DMs** "
                f"{U.yes_no_emoji(self._dm_pref)}\n"
                f"({(await self.user).mention})"
            )
        else:
            dm_text += (
                f"**Not accepting staffing-oriented DMs** "
                f"{U.yes_no_emoji(self._dm_pref)}"
            )
        dm_text += f"\n{U.draw_line(extra=25)}"

        raw_genre_list = sorted(
            [genre.proper_name for genre in self._genres],
            key=lambda genre: genre.lower()
        )
        genres1, genres2, genres3 = U.list_to_columns(raw_genre_list, 3)

        raw_links = self.links.links_list()
        links1, links2 = U.list_to_columns(raw_links, 2, add_markdown=False)

        return U.make_embed(
            title=f"{self.name}'s Profile",
            description=dm_text,
            color=self.color,
            fields=[
                EmbedField(
                    name="__Accent Color__",
                    value=(
                        f"{BotEmojis.ArrowLeft} -- (__{str(self.color).upper()}__)"
                        if self.color is not None
                        else "`Not Set`"
                    ),
                    inline=True
                ),
                EmbedField(
                    name=f"{BotEmojis.No18} __NSFW Music__ {BotEmojis.No18}",
                    value=U.yes_no_emoji(self._nsfw),
                    inline=True
                ),
                EmbedField(
                    name=f"{BotEmojis.FlyingMoney} __Rates__ {BotEmojis.FlyingMoney}",
                    value=(self.rates or "`Not set`") + f"\n{U.draw_line(extra=15)}",
                    inline=False
                ),
                EmbedField(
                    name=f"{BotEmojis.EarbudLeft} __Genres__ {BotEmojis.EarbudRight}",
                    value=genres1,
                    inline=True
                ),
                EmbedField("** **", genres2, inline=True),
                EmbedField("** **", genres3, inline=True),
                EmbedField(U.draw_line(extra=15), "", inline=False),
                EmbedField(
                    name=f"{BotEmojis.GenericLinkIcon} __Links__ {BotEmojis.GenericLinkIcon}",
                    value=links1,
                    inline=True
                ),
                EmbedField("** **", links2, True),
                EmbedField(U.draw_line(extra=15), "", inline=False),
                EmbedField(
                    name=f"{BotEmojis.CalendarLogo} __Availability__ {BotEmojis.CalendarLogo}",
                    value=(
                        DJAvailability.short_availability_status(self.availability) +
                        f"\n{U.draw_line(extra=15)}"
                    ),
                    inline=True,
                ),
                EmbedField(
                    name=f"{BotEmojis.World} __Home Region(s)__ {BotEmojis.World}",
                    value=(
                        ", ".join([region.abbreviation for region in self._regions])
                        if self._regions
                        else "`Not set`"
                    ),
                    inline=True
                ),
                EmbedField(
                    name=f"{BotEmojis.Scroll} __About Me__ {BotEmojis.Scroll}",
                    value=U.string_clamp(self.aboutme, 100) or "`Not set`",
                    inline=False
                )
            ],
            thumbnail_url=self.images.logo,
        )

################################################################################
    async def compile(self) -> Tuple[Embed, Embed, Optional[Embed]]:

        dm_text = f"{U.yes_no_emoji(self._dm_pref)} "
        if self._dm_pref:
            dm_text += (
                f"**Accepting staffing-oriented DMs** "
                f"{U.yes_no_emoji(self._dm_pref)}\n"
                f"({(await self.user).mention})"
            )
        else:
            dm_text += (
                f"**Not accepting staffing-oriented DMs** "
                f"{U.yes_no_emoji(self._dm_pref)}"
            )
        dm_text += f"\n{U.draw_line(extra=25)}"

        raw_genre_list = sorted(
            [genre.proper_name for genre in self._genres],
            key=lambda genre: genre.lower()
        )
        genres1, genres2, genres3 = U.list_to_columns(raw_genre_list, 3)

        raw_links = self.links.links_list()
        links1, links2 = U.list_to_columns(raw_links, 2, add_markdown=False)

        main_profile = U.make_embed(
            title=self.name,
            description=dm_text,
            color=self.color,
            fields=[

                EmbedField(
                    name=f"{BotEmojis.FlyingMoney} __Rates__ {BotEmojis.FlyingMoney}",
                    value=(self.rates or "`Not set`"),
                    inline=True
                ),
                EmbedField(
                    name=f"{BotEmojis.World} __Home Region(s)__ {BotEmojis.World}",
                    value=", ".join([region.abbreviation for region in self._regions]),
                    inline=True
                ),
                EmbedField(U.draw_line(extra=15), "", inline=False),
                EmbedField(
                    name=f"{BotEmojis.EarbudLeft} __Genres__ {BotEmojis.EarbudRight}",
                    value=genres1,
                    inline=True
                ),
                EmbedField("** **", genres2, inline=True),
                EmbedField("** **", genres3, inline=True),
                EmbedField(U.draw_line(extra=15), "", inline=False),
                EmbedField(
                    name=f"{BotEmojis.GenericLinkIcon} __Links__ {BotEmojis.GenericLinkIcon}",
                    value=links1,
                    inline=True
                ),
                EmbedField("** **", links2, True),
                EmbedField(U.draw_line(extra=15), "", inline=False),
                EmbedField(
                    name=f"{BotEmojis.No18} __NSFW Music__ {BotEmojis.No18}",
                    value=U.yes_no_emoji(self._nsfw),
                    inline=True
                )
            ],
            thumbnail_url=self.images.logo
        )

        availability = U.make_embed(
            title=f"{self.name}'s Availability",
            description=DJAvailability.long_availability_status(self.availability),
            color=self.color,
            footer_text=self.links.twitch_link,
        )

        aboutme = U.make_embed(
            color=self.color,
            title=f"About {self.name}",
            description=self.aboutme,
            footer_text=self.links.twitch_link,
        ) if self.aboutme is not None else None

        return main_profile, availability, aboutme

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        return DJProfileStatusView(user, self)

################################################################################
    async def set_color(self, interaction: Interaction) -> None:

        modal = AccentColorModal(self._color)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.color = modal.value
        await self.update_post_components()

################################################################################
    async def set_name(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title=f"Set Profile Name",
            attribute="Name",
            cur_val=self._name,
            example="eg. 'DJ Frogge'",
            max_length=100
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.name = modal.value
        await self.update_post_components()

################################################################################
    async def toggle_nsfw(self, interaction: Interaction) -> None:

        self.nsfw = not self._nsfw
        await interaction.edit()
        await self.update_post_components()

################################################################################
    async def set_aboutme(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Profile About Me",
            attribute="About Me",
            cur_val=self._aboutme,
            example="eg. 'I love playing music and frogs!'",
            max_length=4000,
            required=False,
            multiline=True
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.aboutme = modal.value
        await self.update_post_components()

################################################################################
    async def set_rates(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set DJ Profile Rates",
            attribute="Rates",
            cur_val=self._rates,
            example="eg. '10m gil per hour'",
            max_length=400,
            required=False,
            multiline=True
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.rates = modal.value
        await self.update_post_components()

################################################################################
    async def toggle_dm_pref(self, interaction: Interaction) -> None:

        self.dm_pref = not self._dm_pref
        await interaction.edit()
        await self.update_post_components()

################################################################################
    async def set_genres(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Set Genres",
            description=(
                "Please select your genres from the list below.\n\n"
                
                "You may select multiple genres."
            )
        )
        view = FroggeSelectView(interaction.user, MusicGenre.select_options(), multi_select=True)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.genres = [MusicGenre(int(genre)) for genre in view.value]
        await self.update_post_components()

################################################################################
    async def set_regions(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Select Your Home Region(s)",
            description=(
                "Pick your character's home region(s) from the drop-down below."
            )
        )
        view = FroggeSelectView(interaction.user, XIVRegion.select_options(), multi_select=True)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.regions = [XIVRegion(int(dc)) for dc in view.value]
        await self.update_post_components()

################################################################################
    async def links_menu(self, interaction: Interaction) -> None:

        await self.links.menu(interaction)

################################################################################
    async def images_menu(self, interaction: Interaction) -> None:

        await self.images.menu(interaction)

################################################################################
    async def set_timezone(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Set Timezone",
            description="Please select your timezone from the picker below."
        )
        view = FroggeSelectView(interaction.user, Timezone.select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.timezone = U.TIMEZONE_OFFSETS[Timezone(int(view.value))]

################################################################################
    async def set_availability(self, interaction: Interaction) -> None:

        if self._tz is None:
            await self.set_timezone(interaction)
            if self._tz is None:
                return

        prompt = U.make_embed(
            title="Set Availability",
            description="Please select the day you want to set availability for."
        )
        view = FroggeSelectView(interaction.user, Weekday.select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        weekday = Weekday(int(view.value))
        assert self._tz is not None

        prompt = U.make_embed(
            title="Set Availability Start",
            description=(
                f"Please select the beginning of your availability "
                f"for `{weekday.proper_name}`...\n\n"
                
                f"Times will be interpreted using the previously configured "
                f"`{self._tz.key}` timezone."
            )
        )
        view = TimeSelectView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        for i, a in enumerate(self._availability):
            if a.day == weekday:
                self._availability.pop(i).delete()
                break

        if view.value is Hours.Unavailable:
            return

        start_hour, start_minute = view.value

        prompt = U.make_embed(
            title="Set Availability End",
            description=(
                f"Please select the end of your availability "
                f"for `{weekday.proper_name}`...\n\n"

                f"Times will be interpreted using the previously configured "
                f"`{self._tz.key}` timezone."
            )
        )
        view = TimeSelectView(interaction.user, False)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        end_hour, end_minute = view.value

        # 1) Figure out a date in local time for the chosen weekday
        #    This is optional, but if you want to handle the user picking e.g. "Wednesday"
        #    and it's currently "Sunday" in their local TZ, find the next Wednesday, etc.
        now_local = datetime.now(self._tz)
        today_local = now_local.date()
        # Python's datetime.weekday(): Monday=0..Sunday=6
        current_wkday = now_local.weekday()
        day_diff = (weekday.value - current_wkday) % 7
        chosen_date_local = today_local + timedelta(days=day_diff)

        # 2) Construct naive datetimes for the chosen date + user input hours/minutes
        start_naive = datetime(chosen_date_local.year, chosen_date_local.month, chosen_date_local.day,
                               start_hour, start_minute)
        end_naive = datetime(chosen_date_local.year, chosen_date_local.month, chosen_date_local.day,
                             end_hour, end_minute)

        # 3) Attach the user’s time zone (i.e., interpret these naive datetimes as local time)
        start_with_tz = start_naive.replace(tzinfo=self._tz)
        end_with_tz   = end_naive.replace(tzinfo=self._tz)

        # 4) Convert to UTC
        start_utc = start_with_tz.astimezone(ZoneInfo("UTC"))
        end_utc   = end_with_tz.astimezone(ZoneInfo("UTC"))

        # 5) Store the UTC times
        availability = DJAvailability.new(
            self,
            weekday,
            start_utc.hour,
            start_utc.minute,
            end_utc.hour,
            end_utc.minute
        )
        self._availability.append(availability)

        await self.update_post_components()

################################################################################
    def is_complete(self) -> bool:

        return all([
            self._name,
            self._availability,
            self._regions
        ])

################################################################################
    async def get_tags(self) -> List[ForumTag]:

        post_message = await self.post_message
        post_channel = await self.bot.dj_profile_manager.post_channel

        if post_message is None or post_channel is None:
            return []

        # Tags - Start with DM status
        tag_text = "Accepting DMs" if self.dm_pref else "Not Accepting DMs"
        tags = [
            t for t in post_channel.available_tags
            if t.name.lower() == tag_text.lower()
        ]

        return tags

################################################################################
    async def post(self, interaction: Interaction) -> None:

        await interaction.response.defer(invisible=False, ephemeral=True)

        post_channel = await self.bot.dj_profile_manager.post_channel
        if post_channel is None:
            error = U.make_error(
                title="Profile Posting Channel Not Set",
                message="The DJ profile posting channel has not been set for this server.",
                solution=(
                    "Please contact a server administrator to set the "
                    "DJ profile posting channel."
                )
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        if not self.is_complete():
            error = U.make_error(
                title="Profile Incomplete",
                message="Your profile is incomplete and cannot be posted.",
                solution=(
                    "Please ensure that all of the Main Information required fields are "
                    "filled out and try again:\n"
                    "- Name\n"
                    "- Availability\n"
                    "- Home Region(s)"
                )
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        main_profile, availability, aboutme = await self.compile()
        if len(main_profile) > 5999:
            error = U.make_error(
                title="Profile Too Large!",
                description=f"Current Character Count: `{len(main_profile)}`.",
                message=(
                    "Your profile is larger than Discord's mandatory 6,000-character "
                    "limit for embedded messages."
                ),
                solution=(
                    "The total number of characters in all your profile's sections "
                    "must not exceed 6,000."
                )
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        if await self.update_post_components():
            await interaction.respond(embed=self.success_message())
            return

        # Prepare embeds and persistent view
        embeds = [main_profile, availability] + ([aboutme] if aboutme else [])

        # Handling threads
        matching_thread = next((t for t in post_channel.threads if t.name.lower() == self.name.lower()), None)
        applied_tags = await self.get_tags()
        if matching_thread:
            # Clear the matching thread
            await matching_thread.edit(applied_tags=applied_tags)
            async for m in matching_thread.history():
                await m.delete()
            action = matching_thread.send  # type: ignore
        else:
            # Or create a new thread if no matching one
            action = lambda **kw: post_channel.create_thread(name=self.name, applied_tags=applied_tags, **kw)

        # Post or create thread and handle permissions error
        try:
            result = await action(embeds=embeds)
            if isinstance(result, Thread):
                self.post_message = await result.fetch_message(result.last_message_id)
            else:
                self.post_message = result
        except Forbidden:
            error = InsufficientPermissions(post_channel, "Send Messages")
            await interaction.respond(embed=error, ephemeral=True)
        else:
            await interaction.respond(embed=self.success_message())

################################################################################
    async def update_tags(self, _retry: bool = False) -> bool:

        post_message = await self.post_message
        if post_message is None or (await self.bot.dj_profile_manager.post_channel) is None:
            return False

        assert isinstance(post_message.channel, Thread)

        try:
            await post_message.channel.edit(applied_tags=await self.get_tags())
        except NotFound:
            return False
        except HTTPException as ex:
            if ex.code != 50083 and not _retry:
                print(ex)
                return False
            await post_message.channel.send("Hey Ur Cute", delete_after=0.1)
            await self.update_tags(_retry=True)
            return False
        else:
            return True

################################################################################
    async def update_post_components(self, _retry: bool = False) -> bool:

        post_message = await self.post_message
        if post_message is None:
            return False

        if not await self.update_tags():
            return False

        main_profile, availability, aboutme = await self.compile()
        embeds = [main_profile, availability] + ([aboutme] if aboutme else [])

        try:
            await post_message.edit(embeds=embeds)
        except NotFound:
            self.post_message = None
            return False
        except HTTPException as ex:
            if ex.code != 50083 and not _retry:
                print(ex)
                return False
            await post_message.channel.send("Hey Ur Cute", delete_after=0.1)
            await self.update_post_components(_retry=True)
            return False
        else:
            return True

################################################################################
    def success_message(self) -> Embed:

        return U.make_embed(
            color=FroggeColor.brand_green(),
            title="Profile Posted!",
            description=(
                "Hey, good job, you did it! Your profile was posted successfully!\n"
                f"{U.draw_line(extra=37)}\n"
                f"(__Name:__ ***{self.name}***)\n\n"

                f"{BotEmojis.ArrowRight}  [Check It Out HERE!]"
                f"({self.post_url})  {BotEmojis.ArrowLeft}\n"
                f"{U.draw_line(extra=16)}"
            ),
            thumbnail_url=BotImages.ThumbsUpFrog,
            timestamp=True
        )

################################################################################
