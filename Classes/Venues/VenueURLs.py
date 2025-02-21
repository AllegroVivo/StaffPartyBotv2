from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar, Any, Dict

from discord import EmbedField, Interaction

from UI.Common import BasicTextModal
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import Venue, XIVVenue
################################################################################

__all__ = ("VenueURLs",)

VD = TypeVar("VD", bound="VenueDetails")

################################################################################
class VenueURLs:

    __slots__ = (
        "_parent",
        "logo",
        "discord",
        "website",
        "banner",
        "application",
    )

################################################################################
    def __init__(self,  parent: Venue, **kwargs) -> None:

        self._parent: Venue = parent

        self.discord: Optional[str] = kwargs.get("discord_url")
        self.website: Optional[str] = kwargs.get("website_url")
        self.logo: Optional[str] = kwargs.get("logo_url")
        self.banner: Optional[str] = kwargs.get("banner_url")
        self.application: Optional[str] = kwargs.get("app_url")

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "discord_url": self.discord,
            "website_url": self.website,
            "logo_url": self.logo,
            "banner_url": self.banner,
            "app_url": self.application
        }

################################################################################
    def update_from_xiv_venue(self, xiv_venue: XIVVenue) -> None:

        self.discord = xiv_venue.discord
        self.website = xiv_venue.website
        self.banner = xiv_venue.banner

################################################################################
    def field(self) -> EmbedField:

        value = (self.discord or '`Not Set`') + "\n\n"
        value += "__**Webpage**__\n"
        value += (self.website or '`Not Set`') + "\n\n"
        value += "__**Staff Application**__\n"
        value += (self.application or '`Not Set`')

        return EmbedField(
            name="__Discord Server__",
            value=f"{value}\n{U.draw_line(extra=15)}",
            inline=True,
        )

################################################################################
    async def set_logo(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Set Venue Logo",
            description="Please upload an image for the venue's logo.",
        )
        image_url = await U.wait_for_image(interaction, prompt)
        if image_url is None:
            return

        self.logo = image_url
        self._parent.update()

################################################################################
    async def set_application_url(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Staff Application URL",
            attribute="URL",
            cur_val=self.application,
            max_length=250,
            required=False,
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.application = modal.value
        self._parent.update()

################################################################################
