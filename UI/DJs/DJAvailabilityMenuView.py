from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle

from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import DJLinkManager
################################################################################

__all__ = ("DJAvailabilityMenuView",)

################################################################################        
class DJAvailabilityMenuView(FroggeView):

    def __init__(self, user: User, links: DJLinkManager):

        super().__init__(user, links)

        button_list = [
            AddLinkButton(),
            RemoveLinkButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)
            
        self.set_button_attributes()

################################################################################
class AddLinkButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            label="Add Link",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.links)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.add_link(interaction)
        await self.view.edit_message_helper(interaction=interaction, embed=self.view.ctx.status())

################################################################################
class ModifyButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            label="Add Link",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.links)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.add_link(interaction)
        await self.view.edit_message_helper(interaction=interaction, embed=self.view.ctx.status())

################################################################################
class RemoveLinkButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Link",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.disabled = len(self.view.ctx.links) == 0
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.remove_link(interaction)
        await self.view.edit_message_helper(interaction=interaction, embed=self.view.ctx.status())
        
################################################################################
