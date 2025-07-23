from __future__ import annotations

from discord import Interaction, ButtonStyle
from discord.ui import View

from UI.Common import CloseMessageButton, FroggeButton
################################################################################

__all__ = ("NoServicesAddView",)

################################################################################
class NoServicesAddView(View):

    def __init__(self):
        
        super().__init__()
        
        button_list = [
            AddRequestButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class AddRequestButton(FroggeButton):
    
    def __init__(self):
        
        super().__init__(
            style=ButtonStyle.success,
            label="Add a New Service Request!",
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        await self.view.ctx.request_wizard(interaction)

        await self.view.update(
            pages=await self.view.ctx.make_pages(interaction.user.id),
            current_page=self.view.current_page
        )
        
################################################################################
