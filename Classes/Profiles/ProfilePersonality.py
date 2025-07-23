from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Dict, Any

from discord import Embed, User, EmbedField, Interaction

from Assets import BotEmojis
from UI.Profiles import ProfilePersonalityStatusView
from .ProfileSection import ProfileSection
from Utilities import Utilities as U
from UI.Common import BasicTextModal, InstructionsInfo

if TYPE_CHECKING:
    from Classes import Profile
    from UI.Common import FroggeView
################################################################################

__all__ = ("ProfilePersonality", )

################################################################################
class ProfilePersonality(ProfileSection):

    __slots__ = (
        "_likes",
        "_dislikes",
        "_personality",
        "_aboutme",
    )

################################################################################
    def __init__(self, parent: Profile, **kwargs) -> None:

        super().__init__(parent)

        self._likes: List[str] = kwargs.get("likes", [])
        self._dislikes: List[str] = kwargs.get("dislikes", [])
        self._personality: Optional[str] = kwargs.get("personality")
        self._aboutme: Optional[str] = kwargs.get("about_me")

################################################################################
    @property
    def likes(self) -> List[str]:

        return self._likes

    @likes.setter
    def likes(self, value: List[str]) -> None:

        self._likes = value
        self.update()

################################################################################
    @property
    def dislikes(self) -> List[str]:

        return self._dislikes

    @dislikes.setter
    def dislikes(self, value: List[str]) -> None:

        self._dislikes = value
        self.update()

################################################################################
    @property
    def personality(self) -> Optional[str]:

        return self._personality

    @personality.setter
    def personality(self, value: Optional[str]) -> None:

        self._personality = value
        self.update()

###############################################################################
    @property
    def about_me(self) -> Optional[str]:

        return self._aboutme

    @about_me.setter
    def about_me(self, value: Optional[str]) -> None:

        self._aboutme = value
        self.update()

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "likes": self._likes,
            "dislikes": self._dislikes,
            "personality": self._personality,
            "about_me": self._aboutme
        }

################################################################################
    def status(self) -> Embed:

        if self.about_me is None:
            aboutme_value = "`Not Set`"
        elif len(self.about_me) < 250:
            aboutme_value = self.about_me
        else:
            aboutme_value = self.about_me[:251] + "...\n*(Preview Only -- Click below to see the whole thing!)*"

        return U.make_embed(
            color=self.parent.color,
            title=f"Personality Attributes for __{self.parent.char_name}__",
            description=U.draw_line(extra=40),
            fields=[
                self._likes_field(),
                self._dislikes_field(),
                self._personality_field(),
                EmbedField(
                    name=f"{BotEmojis.Scroll}  __About Me / Biography__  {BotEmojis.Scroll}",
                    value=f"{aboutme_value}\n{U.draw_line(extra=15)}",
                    inline=False
                )
            ]
        )

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        return ProfilePersonalityStatusView(user, self)

################################################################################
    def compile(self) -> Any:

        return (
            self._likes_field() if self.likes else None,
            self._dislikes_field() if self.dislikes else None,
            self._personality_field() if self.personality else None,
            U.make_embed(
                color=self.parent.color,
                title=f"About {self.parent.char_name}",
                description=self.about_me,
                footer_text=(
                    self.parent._main_info.custom_url
                    if self.parent._main_info.custom_url is not None
                    else None
                )
            ) if self.about_me is not None else None
        )

################################################################################
    def progress(self) -> str:

        return (
            f"{U.draw_line(extra=15)}\n"
            "__**Personality**__\n"
            f"{self.progress_emoji(self._likes)} -- Likes\n"
            f"{self.progress_emoji(self._dislikes)} -- Dislikes\n"
            f"{self.progress_emoji(self._personality)} -- Personality\n"
            f"{self.progress_emoji(self._aboutme)} -- About Me\n"
        )

################################################################################
    def _likes_field(self) -> EmbedField:

        likes_list = "\n".join([f"- {l}" for l in self.likes])
        return EmbedField(
            name=f"{BotEmojis.Check}  __Likes__",
            value=(likes_list + f"\n{U.draw_line(extra=14)}") if self.likes else "`Not Set`",
            inline=True
        )

################################################################################
    def _dislikes_field(self) -> EmbedField:

        return EmbedField(
            name=f"{BotEmojis.Cross}  __Dislikes__",
            value="\n".join([f"- {d}" for d in self.dislikes]) if self.dislikes else "`Not Set`",
            inline=True
        )

################################################################################
    def _personality_field(self) -> EmbedField:

        return EmbedField(
            name=f"{BotEmojis.Goose}  __Personality__  {BotEmojis.Goose}",
            value=(
                f"{self.personality if self.personality else '`Not Set`'}\n"
                f"{U.draw_line(extra=15)}"
            ),
            inline=False
        )

################################################################################
    async def set_likes(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Profile Likes",
            attribute="Likes List",
            cur_val=", ".join(self.likes) if self.likes else None,
            example="eg. 'Moist Climates, Long Walks Around the Pond, Flies'",
            max_length=300,
            required=False,
            multiline=True,
            instructions=InstructionsInfo(
                placeholder="Enter your Likes list below.",
                value=(
                    f"Enter a list of your likes separated by commas. Minimum "
                    f"three is suggested. Your likes list should be LONGER "
                    f"than your dislikes to avoid formatting issues."
                )
            )
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.likes = [l.strip() for l in modal.value.split(",")] if modal.value else []
        await self.update_post_components()

################################################################################
    async def set_dislikes(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Profile Dislikes",
            attribute="Dislikes List",
            cur_val=", ".join(self.dislikes) if self.dislikes else None,
            example="eg. 'Dry Climates, Braggarts, Humans'",
            max_length=300,
            required=False,
            multiline=True,
            instructions=InstructionsInfo(
                placeholder="Enter your Dislikes list below.",
                value=(
                    f"Enter a list of your dislikes separated by commas. Minimum "
                    f"three is suggested. Your dislikes list should be SHORTER "
                    f"than your likes to avoid formatting issues."
                )
            )
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.dislikes = [l.strip() for l in modal.value.split(",")] if modal.value else []
        await self.update_post_components()

################################################################################
    async def set_personality(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Profile Personality",
            attribute="Personality",
            cur_val=self.personality,
            example="eg. 'Curious, Playful, Mischievous'",
            max_length=300,
            required=False,
            multiline=True,
            instructions=InstructionsInfo(
                placeholder="Enter your Personality traits below.",
                value=(
                    f"Enter your desired Personality section content here. "
                    "Note that this accepts markdown, newlines, and emojis, "
                    "so really make it your own. ♥"
                )
            )
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.personality = modal.value
        await self.update_post_components()

################################################################################
    async def set_aboutme(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Profile About Me",
            attribute="About Me",
            cur_val=self.about_me,
            example="eg. 'I'm a goose who loves to swim and honk.'",
            max_length=3500,
            required=False,
            multiline=True,
            instructions=InstructionsInfo(
                placeholder="Enter your About Me content below.",
                value=(
                    f"Enter your desired About Me / Biography content here. "
                    "Note that this accepts markdown, newlines, and emojis, "
                    "so really make it your own. ♥"
                )
            )
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.about_me = modal.value
        await self.update_post_components()

################################################################################
