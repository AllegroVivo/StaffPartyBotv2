from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button, View

if TYPE_CHECKING:
    from Classes import BGCheck
################################################################################

__all__ = ("BGCheckApprovalView",)

################################################################################
class BGCheckApprovalView(View):

    def __init__(self, bg_check: BGCheck):
        
        super().__init__(timeout=None)
        
        self.bg_check: BGCheck = bg_check

        if not self.bg_check.approved:
            self.add_item(ApproveButton(bg_check.user_id))

################################################################################
class ApproveButton(Button):
    
    def __init__(self, user_id: int):
        
        super().__init__(
            style=ButtonStyle.success,
            label="Approve",
            disabled=False,
            row=0,
            custom_id=f"approve_bg_check_{user_id}"
        )
        
    async def callback(self, interaction):
        await self.view.bg_check.approve(interaction.user)
        await interaction.edit(view=None)
        self.view.stop()
        
################################################################################
