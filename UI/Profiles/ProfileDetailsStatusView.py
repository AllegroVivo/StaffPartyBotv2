from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import ProfileMainInfo
################################################################################

__all__ = ("ProfileDetailsStatusView",)

################################################################################        
class ProfileDetailsStatusView(FroggeView):

    def __init__(self, user: User, details: ProfileMainInfo):

        super().__init__(user, details)

        button_list = [
            NameButton(),
            PositionsButton(),
            SetTrainingsButton(),
            SetRegionsButton(),
            SetRPPrefButton(),
            SetPreferredTagsButton(),
            ToggleNSFWButton(),
            SetAvailabilityButton(),
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
class PositionsButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Qualified Positions",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.positions)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_positions(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class SetTrainingsButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Desired Trainings",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.trainings)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_trainings(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

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
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class SetRPPrefButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="RP Preference",
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.rp_level)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_rp_level(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class SetPreferredTagsButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Preferred Tags",
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.preferred_tags)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_tags(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class ToggleNSFWButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            disabled=False,
            row=1
        )

    def set_attributes(self) -> None:
        if self.view.ctx.nsfw_preference:
            self.style = ButtonStyle.success
            self.label = "NSFW Is Okay"
            self.emoji = BotEmojis.ThumbsUp
        else:
            self.style = ButtonStyle.secondary
            self.label = "No NSFW Please"
            self.emoji = BotEmojis.AgeRestricted

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.toggle_nsfw(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class SetAvailabilityButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Set Availability",
            disabled=False,
            row=2
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
            row=2
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
        await self.view.ctx.toggle_dm_preference(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
