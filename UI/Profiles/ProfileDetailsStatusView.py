from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import ProfileDetails
################################################################################

__all__ = ("ProfileDetailsStatusView",)

################################################################################        
class ProfileDetailsStatusView(FroggeView):

    def __init__(self, user: User, details: ProfileDetails):

        super().__init__(user, details)

        button_list = [
            NameButton(),
            CustomURLButton(),
            ColorButton(),
            SetAvailabilityButton(),
            JobsButton(),
            RatesButton(),
            PositionsButton(),
            ToggleDMPrefButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################        
class NameButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Character Name",
            disabled=False,
            row=0
        )
        
    def set_attributes(self) -> None:
        self.set_style(self.view.ctx._name)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_name(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class CustomURLButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Custom URL",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.url)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_url(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class ColorButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Accent Color",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx._color)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_color(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class JobsButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="RP Jobs",
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.jobs)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_jobs(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class RatesButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Freelance Rates",
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.rates)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_rates(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class PositionsButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Employable Positions",
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.positions)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_positions(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class SetAvailabilityButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Set Availability",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.availability)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_availability(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class ToggleDMPrefButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        if self.view.ctx.dm_preference:
            self.style = ButtonStyle.success
            self.label = "Accepting DMs"
            self.emoji = BotEmojis.ThumbsUp
        else:
            self.style = ButtonStyle.danger
            self.label = "Not Accepting DMs"
            self.emoji = BotEmojis.ThumbsDown
        
    async def callback(self, interaction: Interaction) -> None:
        self.view.ctx.toggle_dm_preference()
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
