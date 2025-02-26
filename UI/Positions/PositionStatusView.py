from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Any

from discord import Interaction, Role, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import Position, GuildData
################################################################################

__all__ = ("PositionStatusView",)

################################################################################
class PositionStatusView(FroggeView):

    def __init__(self, user: User, position: Position):
        
        super().__init__(user, position)

        button_list = [
            SetNameButton(),
            SetDescriptionButton(),
            SetRoleButton(),
            AddRequirementButton(),
            ModifyRequirementButton(),
            RemoveRequirementButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)
            
        self.set_button_attributes()
            
################################################################################
class SetNameButton(FroggeButton):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Edit Name",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.ctx.set_name(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())
        
################################################################################
class SetRoleButton(FroggeButton):
    
    def __init__(self):
        
        super().__init__(
            label="Edit Role",
            disabled=False,
            row=0
        )
        
    def set_attributes(self) -> None:
        self.set_style(self.view.ctx._role.id)
        
    async def callback(self, interaction):
        await self.view.ctx.set_role(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())
        
################################################################################
class SetDescriptionButton(FroggeButton):

    def __init__(self):

        super().__init__(
            label="Edit Description",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.description)

    async def callback(self, interaction):
        await self.view.ctx.set_description(interaction)
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
