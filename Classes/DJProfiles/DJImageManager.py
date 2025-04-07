from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import Embed, Interaction, EmbedField

from Assets import BotEmojis, BotImages
from UI.Common import ConfirmCancelView
from UI.DJs import DJProfileImagesStatusView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import DJProfile
################################################################################

__all__ = ("DJImageManager", )

################################################################################
class DJImageManager:

    __slots__ = (
        "_parent",
        "_logo",
        "_banner",
    )

################################################################################
    def __init__(self, parent: DJProfile, **kwargs) -> None:

        self._parent: DJProfile = parent

        self._logo: Optional[str] = kwargs.get("logo_url")
        self._banner: Optional[str] = kwargs.get("image_url")

################################################################################
    @property
    def logo(self) -> Optional[str]:

        return self._logo

    @logo.setter
    def logo(self, logo: Optional[str]) -> None:

        self._logo = logo
        self.update()

################################################################################
    @property
    def banner(self) -> Optional[str]:

        return self._banner

    @banner.setter
    def banner(self, banner: Optional[str]) -> None:

        self._banner = banner
        self.update()

################################################################################
    def update(self) -> None:

        self._parent.update()

################################################################################
    def status(self) -> Embed:
        return U.make_embed(
            color=self._parent.color,
            title=f"Image Details for `{self._parent.name}`",
            description=(
                "The buttons below allow you to change or remove an image "
                "attached to your profile."
            ),
            thumbnail_url=self._logo or BotImages.ThumbnailMissing,
            image_url=self._banner or BotImages.MainImageMissing,
            fields=[
                EmbedField(U.draw_line(extra=30), "** **", False),
                EmbedField(
                    name="__Banner__",
                    value=f"-{BotEmojis.ArrowDown}{BotEmojis.ArrowDown}{BotEmojis.ArrowDown}-",
                    inline=True
                ),
                EmbedField("** **", "** **", True),
                EmbedField(
                    name="__Logo__",
                    value=f"-{BotEmojis.ArrowRight}{BotEmojis.ArrowRight}{BotEmojis.ArrowRight}-",
                    inline=True
                ),
            ]
        )

################################################################################
    async def menu(self, interaction: Interaction) -> None:

        embed = self.status()
        view = DJProfileImagesStatusView(interaction.user, self)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    async def set_thumbnail(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Set Profile Thumbnail",
            description="Please provide the image you want to set as your thumbnail."
        )
        image_url = await U.wait_for_image(interaction, prompt)
        if image_url is None:
            return

        self.logo = image_url
        await self._parent.update_post_components()

################################################################################
    async def set_banner(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Set Profile Banner",
            description="Please provide the image you want to set as your banner."
        )
        image_url = await U.wait_for_image(interaction, prompt)
        if image_url is None:
            return

        self.banner = image_url
        await self._parent.update_post_components()

################################################################################
    async def remove_thumbnail(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Remove Profile Thumbnail",
            description="Are you sure you want to remove your profile thumbnail?"
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.logo = None
        await self._parent.update_post_components()

################################################################################
    async def remove_banner(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Remove Profile Banner",
            description="Are you sure you want to remove your profile banner?"
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.banner = None
        await self._parent.update_post_components()

################################################################################
