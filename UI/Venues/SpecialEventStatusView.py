from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import SpecialEvent, VenueTag
################################################################################

__all__ = ("SpecialEventStatusView",)

################################################################################
class SpecialEventStatusView(FroggeView):

    def __init__(self, user: User, event: SpecialEvent) -> None:

        super().__init__(user, event)

        button_list = [
            SetTitleButton(),
            SetDescriptionButton(),
            SetLocationButton(),
            SetStartButton(),
            SetLengthButton(),
            AddLinkButton(),
            RemoveLinkButton(),
            SetRequirementsButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################
class SetTitleButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Set Title",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_title(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class SetDescriptionButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            label="Set Description",
            disabled=False,
            row=0,
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.description)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_description(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class SetLengthButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            label="Set Length",
            row=0,
            disabled=False
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.length)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_length(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class SetStartButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            label="Set Start Time",
            row=0,
            disabled=False
        )
        
    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.start)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_start(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class SetLocationButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            label="Set Location",
            row=0,
            disabled=False
        )
        
    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.location)
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_location(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class AddLinkButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.success,
            label="Add Associated Link",
            row=1,
            disabled=False
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.add_link(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class RemoveLinkButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Associated Link",
            row=1,
            disabled=False
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.remove_link(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class SetRequirementsButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Set Requirements",
            row=1,
            disabled=False
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_requirements(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
