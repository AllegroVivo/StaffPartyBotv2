from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import PositionManager
################################################################################

__all__ = ("PositionManagerMenuView",)

################################################################################
class PositionManagerMenuView(FroggeView):

    def __init__(self, user: User, mgr: PositionManager):
        
        super().__init__(user, mgr)

        button_list = [
            AddPositionButton(),
            ModifyPositionButton(),
            RemovePositionButton(),
            AddRequirementButton(),
            ModifyRequirementButton(),
            RemoveRequirementButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)
            
        self.set_button_attributes()
            
################################################################################
class AddPositionButton(FroggeButton):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.success,
            label="Add Position",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.ctx.add_item(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())
        
################################################################################
class ModifyPositionButton(FroggeButton):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Modify Position",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction):
        await self.view.ctx.modify_item(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())
        
################################################################################
class RemovePositionButton(FroggeButton):

    def __init__(self):

        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Position",
            disabled=False,
            row=0
        )

    async def callback(self, interaction):
        await self.view.ctx.remove_item(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class AddRequirementButton(Button):

    def __init__(self):

        super().__init__(
            style=ButtonStyle.success,
            label="Add Requirement",
            disabled=False,
            row=1
        )

    async def callback(self, interaction: Interaction):
        await self.view.ctx.add_requirement(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class ModifyRequirementButton(Button):

    def __init__(self):

        super().__init__(
            style=ButtonStyle.primary,
            label="Modify Requirement",
            disabled=False,
            row=1
        )

    async def callback(self, interaction: Interaction):
        await self.view.ctx.modify_requirement(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class RemoveRequirementButton(Button):

    def __init__(self):

        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Requirement",
            disabled=False,
            row=1
        )

    async def callback(self, interaction: Interaction):
        await self.view.ctx.remove_requirement(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
