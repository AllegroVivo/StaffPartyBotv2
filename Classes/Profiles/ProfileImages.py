from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, Optional, List, Literal

from discord import User, Embed, EmbedField, Interaction

from Assets import BotEmojis, BotImages
from Errors import MaxItemsReached
from UI.Profiles import SetRemoveImageView, ProfileImagesStatusView
from .ProfileSection import ProfileSection
from .AdditionalImage import AdditionalImage
from Utilities import Utilities as U
from UI.Common import ConfirmCancelView, Frogginator

if TYPE_CHECKING:
    from Classes import Profile
    from UI.Common import FroggeView
################################################################################

__all__ = ("ProfileImages", )

################################################################################
class ProfileImages(ProfileSection):

    __slots__ = (
        "_thumbnail",
        "_main_image",
        "_additional",
        "_adding"
    )

    MAX_ADDITIONAL_IMAGES: int = 3

################################################################################
    def __init__(self, parent: Profile, **kwargs) -> None:

        super().__init__(parent)

        self._thumbnail: Optional[str] = kwargs.get("thumbnail_url")
        self._main_image: Optional[str] = kwargs.get("main_image_url")
        self._additional: List[AdditionalImage] = [
            AdditionalImage(self, **a) for a in kwargs.get("additional_images", [])
        ]
        self._adding: bool = False

################################################################################
    @property
    def thumbnail(self) -> Optional[str]:

        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, value: Optional[str]) -> None:

        self._thumbnail = value
        self.update()

################################################################################
    @property
    def main_image(self) -> Optional[str]:

        return self._main_image

    @main_image.setter
    def main_image(self, value: Optional[str]) -> None:

        self._main_image = value
        self.update()

################################################################################
    @property
    def additional(self) -> List[AdditionalImage]:

        return self._additional

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "thumbnail_url": self._thumbnail,
            "main_image_url": self._main_image,
        }

################################################################################
    def get_additional(self, image_id: int) -> Optional[AdditionalImage]:

        return next((a for a in self._additional if a.id == int(image_id)), None)

################################################################################
    def status(self) -> Embed:

        return U.make_embed(
            color=self.parent._aag.color,
            title=f"Image Details for `{self.parent.char_name}`",
            description=(
                "The buttons below allow you to remove and image attached to your profile\n"
                "or to view a paginated list of your current additional images.\n\n"

                "***To change your thumbnail and main image assets, or to add an additional image\n"
                "to your profile, use the corresponding buttons.***"
            ),
            thumbnail_url=self._thumbnail or BotImages.ThumbnailMissing,
            image_url=self._main_image or BotImages.MainImageMissing,
            timestamp=False,
            fields=[
                EmbedField(U.draw_line(extra=30), "** **", False),
                self.compile_additional() or EmbedField(
                    name="__Additional Images__",
                    value="`Not Set`",
                    inline=False
                ),
                EmbedField(U.draw_line(extra=30), "** **", False),
                EmbedField(
                    name="__Main Image__",
                    value=f"-{BotEmojis.ArrowDown}{BotEmojis.ArrowDown}{BotEmojis.ArrowDown}-",
                    inline=True
                ),
                EmbedField("** **", "** **", True),
                EmbedField(
                    name="__Thumbnail__",
                    value=f"-{BotEmojis.ArrowRight}{BotEmojis.ArrowRight}{BotEmojis.ArrowRight}-",
                    inline=True
                ),
            ]
        )

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        return ProfileImagesStatusView(user, self)

################################################################################
    def compile(self) -> Any:

        return (
            self.thumbnail,
            self.main_image,
            self.compile_additional()
        )

################################################################################
    def progress(self) -> str:

        return (
            f"{U.draw_line(extra=15)}\n"
            "__**Images**__\n"
            f"{self.progress_emoji(self._thumbnail)} -- Thumbnail *(Upper-Right)*\n"
            f"{self.progress_emoji(self._main_image)} -- Main Image *(Bottom-Center)*\n"
            f"{self.progress_emoji(self._additional)} -- (`{len(self.additional)}`) -- Additional Images\n"
        )

################################################################################
    def compile_additional(self) -> Optional[EmbedField]:

        if not self._additional:
            return None

        return EmbedField(
            name=f"{BotEmojis.Camera} __Additional Images__ {BotEmojis.Camera}",
            value="\n".join([image.compile() for image in self._additional]),
            inline=False
        )

################################################################################
    def image_status(self, image_type: Literal["Thumbnail", "Main"]) -> Embed:

        return U.make_embed(
            title=f"__{image_type} Image__",
            description=(
                f"This image is displayed in the "
                f"{'bottom center' if image_type == 'Main' else 'upper-right corner'} "
                f"of your profile.\n"
                "To change this image, use the buttons below."
            ),
            image_url=(self._main_image or BotImages.MainImageMissing) if image_type == "Main" else None,
            thumbnail_url=(self._thumbnail or BotImages.ThumbnailMissing) if image_type == "Thumbnail" else None
        )

################################################################################
    async def thumbnail_management(self, interaction: Interaction) -> None:

        embed = self.image_status("Thumbnail")
        view = SetRemoveImageView(interaction.user, self, "Thumbnail")

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    async def main_image_management(self, interaction: Interaction) -> None:

        embed = self.image_status("Main")
        view = SetRemoveImageView(interaction.user, self, "Main")

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    async def remove_image(self, interaction: Interaction, image_type: Literal["Thumbnail", "Main"]) -> None:

        confirm = U.make_embed(
            color=self.parent.color,
            title="Confirm Image Removal",
            description=(
                "Confirm that you want to remove the attached image from the "
                "corresponding spot on your profile.\n\n"

                "*(It's gone forever and you'll need to re-upload it again if "
                "you change your mind!)*"
            ),
            thumbnail_url=self.thumbnail if image_type == "Thumbnail" else None,
            image_url=self.main_image if image_type == "Main" else None,
            timestamp=False
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.response.send_message(embed=confirm, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        if image_type == "Thumbnail":
            self.thumbnail = None
        else:
            self.main_image = None

        await self.update_post_components()

################################################################################
    async def set_image(self, interaction: Interaction, image_type: Literal["Thumbnail", "Main"]) -> None:

        if self._adding:
            await interaction.respond(
                "You are already in the process of adding an image.",
                ephemeral=True
            )
            return

        self._adding = True
        prompt = U.make_embed(
            title=f"{image_type} Image",
            description=(
                f"Please send the image you would like to set as your {image_type.lower()}.\n"
                "*(This image will be displayed in the "
                f"{'bottom center' if image_type == 'Main' else 'upper-right corner'} "
                "of your profile.)*"
            )
        )

        if image := await U.wait_for_image(interaction, prompt):
            if image_type == "Thumbnail":
                self.thumbnail = image
            else:
                self.main_image = image

        await self.update_post_components()
        self._adding = False

################################################################################
    async def add_additional_image(self, interaction: Interaction) -> None:

        if len(self._additional) >= self.MAX_ADDITIONAL_IMAGES:
            error = MaxItemsReached("Additional Images", self.MAX_ADDITIONAL_IMAGES)
            await interaction.respond(embed=error, ephemeral=True)
            return

        if self._adding:
            await interaction.respond(
                "You are already in the process of adding an additional image.",
                ephemeral=True
            )
            return

        self._adding = True
        prompt = U.make_embed(
            title="__Additional Image__",
            description=(
                "Please send the image you would like to add to your profile.\n"
                "*(This image will be displayed in the additional images section of your profile.)*"
            )
        )

        if image := await U.wait_for_image(interaction, prompt, U.DumpMethod.Cloudinary):
            self._additional.append(AdditionalImage.new(self, image, None))

        await self.update_post_components()
        self._adding = False

################################################################################
    async def paginate_additional(self, interaction: Interaction) -> None:

        pages = [a.page() for a in self._additional]
        frogginator = Frogginator(pages, self, default_button_row=3)
        await frogginator.respond(interaction)

################################################################################
