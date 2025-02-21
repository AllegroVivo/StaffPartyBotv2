from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import Venue, Position, VenueTag
################################################################################

__all__ = ("VenueStatusView",)

################################################################################
class VenueStatusView(FroggeView):

    def __init__(self, user: User, venue: Venue) -> None:

        super().__init__(user, venue)

        button_list = [
            RPLevelButton(),
            ToggleHiringButton(),
            ApplicationURLButton(),
            SetPositionsButton(),
            LogoButton(),
            MuteReportButton(),
            PostVenueButton(),
            UpdateVenueButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################
class RPLevelButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            label="RP Level",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.rp_level)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_rp_level(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class ToggleHiringButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            label="Hiring",
            disabled=False,
            row=0,
        )

    def set_attributes(self) -> None:
        self.style = (
            ButtonStyle.success
            if self.view.ctx.hiring
            else ButtonStyle.danger
        )
        self.emoji = (
            BotEmojis.CheckGreen
            if self.view.ctx.hiring
            else BotEmojis.ThumbsDown
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.toggle_hiring(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())
        
################################################################################
class LogoButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            label="Logo",
            row=0,
            disabled=False
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.urls.logo)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_logo(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())
        
################################################################################
class SetPositionsButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            label="Employed Jobs",
            row=0,
            disabled=False
        )
        
    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.positions)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_positions(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class ApplicationURLButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            label="Application URL",
            row=0,
            disabled=False
        )
        
    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.urls.application)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_application_url(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())
        
################################################################################
class MuteReportButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Muted User Report",
            row=1,
            disabled=False
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.mute_list_report(interaction)
        
################################################################################
class PostVenueButton(Button):

    def __init__(self):

        super().__init__(
            style=ButtonStyle.secondary,
            label="Post This Venue Listing",
            disabled=False,
            row=2,
            emoji=BotEmojis.FlyingEnvelope
        )

    async def callback(self, interaction):
        await self.view.ctx.post(interaction, None)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class UpdateVenueButton(Button):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Update This Venue from FFXIV Venues",
            disabled=False,
            row=2,
            emoji=BotEmojis.Cycle
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        await self.view.ctx.update_from_xiv_venue(interaction)
        
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())
        
################################################################################
