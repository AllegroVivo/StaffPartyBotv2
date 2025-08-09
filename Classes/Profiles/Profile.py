from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Dict, Any, List, Tuple

from discord import (
    User,
    Embed,
    Message,
    EmbedField,
    Interaction,
    HTTPException,
    NotFound,
    Forbidden,
    ForumTag,
    Thread
)
from discord.utils import MISSING

from Assets import BotEmojis, BotImages
from Classes.Common import ManagedObject, LazyUser, LazyMessage
from UI.Profiles import ProfileMainMenuView, ProfileUserMuteView
from .ProfileMainInfo import ProfileMainInfo
from .ProfileAtAGlance import ProfileAtAGlance
from Utilities import Utilities as U, FroggeColor
from .ProfilePersonality import ProfilePersonality
from .ProfileImages import ProfileImages
from Errors import InsufficientPermissions
from Enums import Position, XIVRegion, RPLevel, VenueTag
from UI.Common import CloseMessageView

if TYPE_CHECKING:
    from Classes import ProfileManager, Venue, BGCheck, Availability
    from UI.Common import FroggeView
################################################################################

__all__ = ("Profile", )

P = TypeVar("P", bound="Profile")

################################################################################
class Profile(ManagedObject):

    __slots__ = (
        "_user",
        "_main_info",
        "_aag",
        "_personality",
        "_images",
        "_post_msg",
        "_muted_venue_ids",
        "_bg_check",
    )

################################################################################
    def __init__(self, mgr: ProfileManager, **kwargs) -> None:

        super().__init__(mgr, kwargs["user_id"])

        self._user: LazyUser = LazyUser(self, kwargs["user_id"])
        self._post_msg: LazyMessage = LazyMessage(self, kwargs.get("post_url"))
        self._muted_venue_ids: List[int] = kwargs.get("muted_venue_ids", [])
        self._bg_check: bool = kwargs.get("bg_check_done", False)

        self._main_info: ProfileMainInfo = ProfileMainInfo(self, **kwargs)
        self._aag: ProfileAtAGlance = ProfileAtAGlance(self, **kwargs)
        self._personality: ProfilePersonality = ProfilePersonality(self, **kwargs)
        self._images: ProfileImages = ProfileImages(self, **kwargs)

################################################################################
    @classmethod
    def new(cls: Type[P], mgr: ProfileManager, user_id: int) -> P:

        new_data = mgr.bot.db.insert.profile(user_id)
        return cls(mgr, **new_data)

################################################################################
    @property
    async def user(self) -> User:

        return await self._user.get()

    @property
    def user_id(self) -> int:

        return self._user.id

################################################################################
    @property
    def char_name(self) -> str:

        return self._main_info.name

################################################################################
    @property
    def custom_url(self) -> Optional[str]:

        return self._aag._url

################################################################################
    @property
    def details(self) -> ProfileMainInfo:

        return self._main_info

################################################################################
    @property
    def ataglance(self) -> ProfileAtAGlance:

        return self._aag

################################################################################
    @property
    def color(self) -> FroggeColor:

        return self._aag.accent_color

################################################################################
    @property
    def personality(self) -> ProfilePersonality:

        return self._personality

################################################################################
    @property
    def images(self) -> ProfileImages:

        return self._images

################################################################################
    @property
    def muted_venues(self) -> List[Venue]:

        return [self.bot.venue_manager[vid] for vid in self._muted_venue_ids]

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
    def bg_check(self) -> Optional[BGCheck]:

        return self.bot.bg_check_manager[self.user_id]

################################################################################
    @property
    def availability(self) -> List[Availability]:

        return self._main_info.availability

################################################################################
    @property
    def desired_trainings(self) -> List[Position]:

        return self._main_info.trainings

################################################################################
    @property
    def data_centers(self) -> List[XIVRegion]:

        return self._main_info.regions

################################################################################
    @property
    def rp_level(self) -> Optional[RPLevel]:

        return self._main_info.rp_level

################################################################################
    @property
    def venue_tags(self) -> List[VenueTag]:

        return self._main_info._tags

################################################################################
    @property
    def nsfw_preference(self) -> bool:

        return self._main_info.nsfw_preference

################################################################################
    def update(self) -> None:

        self.bot.db.update.profile(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "post_url": self.post_url,
            "bg_check_done": self._bg_check,
            "muted_venue_ids": self._muted_venue_ids,
        }

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.profile(self.id)
        self._mgr._managed.remove(self)

################################################################################
    def is_complete(self) -> bool:

        return all([
            self._main_info._regions,
            self._main_info._positions,
            self._main_info._availability,
            self._main_info._name,
            self._main_info._rp_level,
            self._main_info._tags
        ])

################################################################################
    async def status(self) -> Embed:

        return U.make_embed(
            title=f"__Profile Menu for `{self.char_name}`__",
            description=(
                "Select a button below to view or edit the corresponding "
                "section of your profile!"
            )
        )

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        return ProfileMainMenuView(user, self)

################################################################################
    async def compile(self) -> Tuple[Embed, Embed, Optional[Embed]]:

        char_name, region_str, availability, dm_pref = self._main_info.compile()
        color, url, jobs, ataglance = self._aag.compile()
        likes, dislikes, personality, aboutme = self._personality.compile()
        thumbnail, main_image, additional_imgs = self._images.compile()

        if char_name is None:
            char_name = f"Character Name: `Not Set`"
        elif url is not None:
            icon = U.get_emoji_for_link(url)
            char_name = f"{icon}  {char_name}  {icon}"

        if dm_pref:
            dm_text = (
                f"{U.yes_no_emoji(dm_pref)} "
                f"**Accepting staffing-oriented DMs** "
                f"{U.yes_no_emoji(dm_pref)}\n"
                f"({(await self.user).mention})"
            )
        else:
            dm_text = (
                f"{U.yes_no_emoji(dm_pref)} "
                f"**Not accepting staffing-oriented DMs** "
                f"{U.yes_no_emoji(dm_pref)}"
            )

        description = dm_text
        if jobs:
            description += (
                f"\n{U.draw_line(text=jobs)}\n"
                f"{jobs}\n"
                f"{U.draw_line(text=jobs)}"
            )
        description += region_str

        fields: List[EmbedField] = []
        if ataglance is not None:
            fields.append(ataglance)
        if likes is not None:
            fields.append(likes)
        if dislikes is not None:
            fields.append(dislikes)
        if personality is not None:
            fields.append(personality)
        if additional_imgs is not None:
            additional_imgs.value += f"\n{U.draw_line(extra=15)}"
            fields.append(additional_imgs)

        main_profile = U.make_embed(
            color=color or FroggeColor.embed_background(),
            title=char_name,
            description=description,
            url=url,
            thumbnail_url=thumbnail,
            image_url=main_image,
            fields=fields
        )

        return main_profile, availability, aboutme

################################################################################
    async def main_details_menu(self, interaction: Interaction) -> None:

        await self._main_info.menu(interaction)

################################################################################
    async def ataglance_menu(self, interaction: Interaction) -> None:

        await self._aag.menu(interaction)

################################################################################
    async def personality_menu(self, interaction: Interaction) -> None:

        await self._personality.menu(interaction)

################################################################################
    async def images_menu(self, interaction: Interaction) -> None:

        await self._images.menu(interaction)

################################################################################
    async def preview_profile(self, interaction: Interaction) -> None:

        main_profile, _, _ = await self.compile()
        view = CloseMessageView(interaction.user)

        await interaction.respond(embed=main_profile, view=view)
        await view.wait()

################################################################################
    async def preview_availability(self, interaction: Interaction) -> None:

        _, availability, _ = await self.compile()
        view = CloseMessageView(interaction.user)

        await interaction.respond(embed=availability, view=view)
        await view.wait()

################################################################################
    async def preview_aboutme(self, interaction: Interaction) -> None:

        _, _, aboutme = await self.compile()
        if aboutme is None:
            error = U.make_error(
                title="About Me Not Set",
                message="You can't view an empty About Me section.",
                solution=(
                    "Use the `Personality` button to set it, then "
                    "try again."
                )
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        view = CloseMessageView(interaction.user)

        await interaction.respond(embed=aboutme, view=view)
        await view.wait()

################################################################################
    async def progress(self , interaction: Interaction) -> None:

        em_final = self._main_info.progress_emoji(await self.post_message)
        progress = U.make_embed(
            color=self._aag.accent_color,
            title="Profile Progress",
            description=(
                self._main_info.progress() +
                self._aag.progress() +
                self._personality.progress() +
                self._images.progress() +
                f"{U.draw_line(extra=15)}\n"
                f"{em_final} -- Finalize"
            ),
            timestamp=False
        )
        view = CloseMessageView(interaction.user)

        await interaction.response.send_message(embed=progress, view=view)
        await view.wait()

################################################################################
    def _get_top_positions(self) -> List[Position]:

        # Map each position to its weight, defaulting to a high number if not found
        weighted_positions = [
            (job, U.JOB_WEIGHTS.get(job, 100))
            for job in self._main_info.positions
        ]

        # Sort positions by weight (ascending order so lower numbers are first)
        weighted_positions.sort(key=lambda x: x[1])

        # Extract the top four jobs (or fewer if less than four are provided)
        return [pos[0] for pos in weighted_positions[:4]]

################################################################################
    async def get_tags(self) -> List[ForumTag]:

        post_message = await self.post_message
        post_channel = await self.bot.profile_manager.post_channel

        if post_message is None or post_channel is None:
            return []

        # Tags - Start with DM status
        tag_text = "Accepting DMs" if self._main_info.dm_preference else "Not Accepting DMs"
        tags = [
            t for t in post_channel.available_tags
            if t.name.lower() == tag_text.lower()
        ]
        # Add position tags according to weights
        top_positions = [p.proper_name.lower() for p in self._get_top_positions()]
        tags += [
            t for t in post_channel.available_tags
            if t.name.lower() in
            top_positions
        ]

        return tags

################################################################################
    async def post(self, interaction: Interaction) -> None:

        await interaction.response.defer(invisible=False, ephemeral=True)

        post_channel = await self.bot.profile_manager.post_channel
        if post_channel is None:
            error = U.make_error(
                title="Profile Posting Channel Not Set",
                message="The profile posting channel has not been set for this server.",
                solution=(
                    "Please contact a server administrator to set the "
                    "profile posting channel."
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
                    "- Employable Positions\n"
                    "- Home Region(s)\n"
                    "- RP Preference\n"
                    "- Preferred Venue Tags"
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

        if await self.update_post_components(True, True):
            await interaction.respond(embed=self.success_message())
            return

        # Prepare embeds and persistent view
        embeds = [main_profile, availability] + ([aboutme] if aboutme else [])
        view = ProfileUserMuteView(self)

        # Handling threads
        matching_thread = next((t for t in post_channel.threads if t.name.lower() == self.char_name.lower()), None)
        applied_tags = await self.get_tags()
        if matching_thread:
            # Clear the matching thread
            await matching_thread.edit(applied_tags=applied_tags)
            async for m in matching_thread.history():
                await m.delete()
            action = matching_thread.send  # type: ignore
        else:
            # Or create a new thread if no matching one
            action = lambda **kw: post_channel.create_thread(name=self.char_name, applied_tags=applied_tags, **kw)

        self.bot.add_view(view)

        # Post or create thread and handle permissions error
        try:
            result = await action(embeds=embeds, view=view)
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
        if post_message is None or (await self.bot.profile_manager.post_channel) is None:
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
    async def update_post_components(
        self,
        update_embeds: bool = False,
        update_view: bool = True,
        _retry: bool = False
    ) -> bool:

        assert update_embeds or update_view

        post_message = await self.post_message
        if post_message is None:
            return False

        if not await self.update_tags():
            return False

        view = ProfileUserMuteView(self)
        self.bot.add_view(view, message_id=post_message.id)

        main_profile, availability, aboutme = await self.compile()
        embeds = [main_profile, availability] + ([aboutme] if aboutme else [])

        try:
            await post_message.edit(
                embeds=embeds if update_embeds else MISSING,
                view=view if update_view else MISSING
            )
        except NotFound:
            self.post_message = None
            return False
        except HTTPException as ex:
            if ex.code != 50083 and not _retry:
                print(ex)
                return False
            await post_message.channel.send("Hey Ur Cute", delete_after=0.1)
            await self.update_post_components(update_embeds, update_view, _retry=True)
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
                f"(__Character Name:__ ***{self.char_name}***)\n\n"

                f"{BotEmojis.ArrowRight}  [Check It Out HERE!]"
                f"({self.post_url})  {BotEmojis.ArrowLeft}\n"
                f"{U.draw_line(extra=16)}"
            ),
            thumbnail_url=BotImages.ThumbsUpFrog,
            timestamp=True
        )

################################################################################
    def mute_venue(self, venue: Venue) -> bool:

        already_muted = venue.id in self._muted_venue_ids
        newly_muted = not already_muted
        dj_profile = self.bot.dj_profile_manager.get_profile(self.user_id)

        if newly_muted:
            self._muted_venue_ids.append(venue.id)

            if dj_profile and venue.id not in dj_profile._muted_venue_ids:
                dj_profile._muted_venue_ids.append(venue.id)
                dj_profile.update()

        else:
            self._muted_venue_ids.remove(venue.id)

            if dj_profile and venue.id in dj_profile._muted_venue_ids:
                dj_profile._muted_venue_ids.remove(venue.id)
                dj_profile.update()

        self.update()
        return newly_muted

################################################################################
    async def mute_list_report(self, interaction: Interaction) -> None:

        embed = U.make_embed(
            title=f"Muted Venues Report",
            description=(
                (
                    "\n".join([f"• {u.name}" for u in self.muted_venues])
                    if self.muted_venues
                    else "`No muted venues`"
                )
                + f"\n{U.draw_line(extra=20)}"
            )
        )
        view = CloseMessageView(interaction.user)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
