from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ButtonStyle, User

from Enums import RoleType
from UI.Common import CloseMessageButton, FroggeButton, FroggeView

if TYPE_CHECKING:
    from Classes import RoleManager
################################################################################

__all__ = ("RoleManagerMenuView",)

################################################################################
class RoleManagerMenuView(FroggeView):

    def __init__(self, owner: User, mgr: RoleManager):
        
        super().__init__(owner, mgr)
        
        button_list = [
            UpdateRoleButton(RoleType.StaffMain, 0),
            UpdateRoleButton(RoleType.StaffNotValidated, 0),
            UpdateRoleButton(RoleType.VenueManagement, 0),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()
        
################################################################################
class UpdateRoleButton(FroggeButton):
    
    def __init__(self, rtype: RoleType, row: int):
        
        super().__init__(
            style=ButtonStyle.primary,
            label=rtype.proper_name.rstrip("Role"),
            disabled=False,
            row=row
        )

        self.role_type: RoleType = rtype

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.get_role(self.role_type).id)

    async def callback(self, interaction):
        await self.view.ctx.set_role(interaction, self.role_type)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())
        
################################################################################
