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
from .ProfileDetails import ProfileDetails
from .ProfileAtAGlance import ProfileAtAGlance
from Utilities import Utilities as U, FroggeColor
from .ProfilePersonality import ProfilePersonality
from .ProfileImages import ProfileImages
from Errors import InsufficientPermissions

if TYPE_CHECKING:
    from Classes import ProfileManager, Position
    from UI.Common import FroggeView, CloseMessageView
################################################################################

__all__ = ("Profile", )

P = TypeVar("P", bound="Profile")

################################################################################
class Profile(ManagedObject):

    __slots__ = (
        "_user",
        "_details",
        "_aag",
        "_personality",
        "_images",
        "_post_msg",
    )

################################################################################
    def __init__(self, mgr: ProfileManager, **kwargs) -> None:

        super().__init__(mgr, kwargs["user_id"])

        self._user: LazyUser = LazyUser(self, kwargs["user_id"])
        self._post_msg: LazyMessage = LazyMessage(self, kwargs.get("post_url"))

        self._details: ProfileDetails = ProfileDetails(self, **kwargs)
        self._aag: ProfileAtAGlance = ProfileAtAGlance(self, **kwargs)
        self._personality: ProfilePersonality = ProfilePersonality(self, **kwargs)
        self._images: ProfileImages = ProfileImages(self, **kwargs)

################################################################################
    @classmethod
    def new(cls: Type[P], mgr: ProfileManager, user: User) -> P:

        new_data = mgr.bot.db.insert.profile(user.id)
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

        return self._details.name

################################################################################
    @property
    def color(self) -> Optional[FroggeColor]:

        return self._details.color

################################################################################
    @property
    def details(self) -> ProfileDetails:

        return self._details

################################################################################
    @property
    def ataglance(self) -> ProfileAtAGlance:

        return self._aag

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
    async def post_message(self) -> Optional[Message]:

        return await self._post_msg.get()

    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:

        self._post_msg.set(value)

    @property
    def post_url(self) -> Optional[str]:

        return self._post_msg.id

################################################################################
    def update(self) -> None:

        self.bot.db.update.profile(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "post_url": self.post_url,
        }

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.profile(self.id)
        self._mgr._managed.remove(self)

################################################################################
    def is_complete(self) -> bool:

        return all([
            self._aag._data_centers,
            self._details._positions,
            self._details._availability,
            self._details._name,
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

        char_name, url, color, jobs, rates_field, availability, dm_pref = self._details.compile()
        ataglance = self._aag.compile()
        likes, dislikes, personality, aboutme = self._personality.compile()
        thumbnail, main_image, additional_imgs = self._images.compile()

        if char_name is None:
            char_name = f"Character Name: `Not Set`"
        elif url is not None:
            char_name = f"{BotEmojis.Envelope}  {char_name}  {BotEmojis.Envelope}"

        if dm_pref:
            dm_text = (
                f"{U.yes_no_emoji(dm_pref)} **Accepting staffing-oriented DMs** {U.yes_no_emoji(dm_pref)}\n"
                f"({(await self.user).mention})"
            )
        else:
            dm_text = f"{U.yes_no_emoji(dm_pref)} **Not accepting staffing-oriented DMs** {U.yes_no_emoji(dm_pref)}"

        description = dm_text
        if jobs:
            description += (
                f"\n{U.draw_line(text=jobs)}\n"
                f"{jobs}\n"
                f"{U.draw_line(text=jobs)}\n"
            )

        fields: List[EmbedField] = []
        if ataglance is not None:
            fields.append(ataglance)
        if rates_field is not None:
            fields.append(rates_field)
        if likes is not None:
            fields.append(likes)
        if dislikes is not None:
            fields.append(dislikes)
        if personality is not None:
            fields.append(personality)
        if additional_imgs is not None:
            additional_imgs.value += U.draw_line(extra=15)
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

        await self._details.menu(interaction)

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

        em_final = self._details.progress_emoji(await self.post_message)
        progress = U.make_embed(
            color=self.color,
            title="Profile Progress",
            description=(
                self._details.progress() +
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
            (job, U.JOB_WEIGHTS.get(job.name.lower(), 100))
            for job in self._details.positions
        ]

        # Sort positions by weight (ascending order so lower numbers are first)
        weighted_positions.sort(key=lambda x: x[1])

        # Extract the top four jobs (or fewer if less than four are provided)
        top_positions = [pos[0] for pos in weighted_positions[:4]]

        return top_positions

################################################################################
    async def get_tags(self) -> List[ForumTag]:

        post_message = await self.post_message
        post_channel = await self.bot.profile_manager.post_channel

        if post_message is None or post_channel is None:
            return []

        # Tags - Start with DM status
        tag_text = "Accepting DMs" if self._details.dm_preference else "Not Accepting DMs"
        tags = [
            t for t in post_channel.available_tags
            if t.name.lower() == tag_text.lower()
        ]
        # Add position tags according to weights
        top_positions = [p.name.lower() for p in self._get_top_positions()]
        tags += [
            t for t in post_channel.available_tags
            if t.name.lower() in
            top_positions
        ]

        return tags

################################################################################
    async def post(self, interaction: Interaction) -> None:

        await interaction.response.defer(invisible=False)

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
                    "Please ensure that all of the following required fields are "
                    "filled out and try again:\n"
                    "- Name *(Main Info)*\n"
                    "- Availability *(Main Info)*\n"
                    "- Employable Positions *(Main Info)*\n"
                    "- Home Region(s) *(At a Glance)*\n"
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
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        member = self.bot.get_guild(self.bot.SPB_ID).get_member(self._user.id)
        post_message = await self.post_message

        if self.bot.DEBUG is False:
            if post_message is None:
                all_pos_roles = [
                    await pos.role for pos in self.bot.position_manager.positions
                    if pos._role.id is not None
                ]
                await member.remove_roles(*all_pos_roles)

                pos_roles = [
                    await pos.role for pos in self._details.positions
                    if pos._role.id is not None
                ]
                await member.add_roles(*pos_roles)

        if await self.update_post_components(True, True):
            await interaction.respond(embed=self.success_message())
            return

        # Prepare embeds and persistent view
        embeds = [main_profile, availability] + ([aboutme] if aboutme else [])
        view = ProfileUserMuteView(self)

        # Handling threads
        channel = self.manager.guild.channel_manager.profiles_channel
        matching_thread = next((t for t in channel.threads if t.name.lower() == self.char_name.lower()), None)

        if matching_thread:
            # Clear the matching thread
            await matching_thread.edit(applied_tags=self.get_tags())
            async for m in matching_thread.history():
                await m.delete()
            action = matching_thread.send  # type: ignore
        else:
            # Or create a new thread if no matching one
            action = lambda **kw: channel.create_thread(name=self.char_name, applied_tags=self.get_tags(), **kw)

        self.bot.add_view(view)

        # Post or create thread and handle permissions error
        try:
            result = await action(embeds=embeds, view=view)
            if isinstance(result, Thread):
                self.post_message = await result.fetch_message(result.last_message_id)
            else:
                self.post_message = result
        except Forbidden:
            error = InsufficientPermissions(channel, "Send Messages")
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
        update_embeds: bool,
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

        main_profile, availability, aboutme = self.compile()
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
