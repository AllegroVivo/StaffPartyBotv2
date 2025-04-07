from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import DJProfile
################################################################################

__all__ = ("DJProfileStatusView",)

################################################################################        
class DJProfileStatusView(FroggeView):

    def __init__(self, user: User, profile: DJProfile):

        super().__init__(user, profile)

        button_list = [
            SetAccentColorButton(),
            SetNameButton(),
            SetGenresButton(),
            SetRatesButton(),
            SetRegionsButton(),
            ToggleNSFWButton(),
            ToggleDMPrefButton(),
            SetAboutMeButton(),
            LinksMenuButton(),
            ImageMenuButton(),
            SetAvailabilityButton(),
            PostProfileButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################
class SetAccentColorButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Set Accent Color",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.color)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_color(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class SetNameButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Set Name",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.name)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_name(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class ToggleNSFWButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        self.style = (
            ButtonStyle.success
            if self.view.ctx.nsfw
            else ButtonStyle.secondary
        )
        self.emoji = (
            BotEmojis.ThumbsUp
            if self.view.ctx.nsfw
            else None
        )
        self.label = (
            "I play NSFW Music"
            if self.view.ctx.nsfw
            else "I play SFW Music"
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.toggle_nsfw(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class SetAboutMeButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Set About Me",
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.aboutme)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_aboutme(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class SetGenresButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Select Genres",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.genres)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_genres(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class LinksMenuButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Manage Links",
            disabled=False,
            row=2
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.links_menu(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class ImageMenuButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Manage Images",
            disabled=False,
            row=2
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.images_menu(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class SetAvailabilityButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Manage Availability",
            disabled=False,
            row=2
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_availability(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class SetRatesButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Set Rates",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.rates)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_rates(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class SetRegionsButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Home Regions",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.regions)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_regions(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class ToggleDMPrefButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Toggle DM Pref",
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        self.style = (
            ButtonStyle.success
            if self.view.ctx.dm_pref
            else ButtonStyle.danger
        )
        self.emoji = (
            BotEmojis.ThumbsUp
            if self.view.ctx.dm_pref
            else None
        )
        self.label = (
            "Accepting DMs"
            if self.view.ctx.dm_pref
            else "Not Accepting DMs"
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.toggle_dm_pref(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class PostProfileButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Post Profile",
            disabled=False,
            row=4,
            emoji=BotEmojis.CheckGreen
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.post(interaction)

################################################################################
