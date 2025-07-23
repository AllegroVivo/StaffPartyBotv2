from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, ButtonStyle
from discord.ui import View

from UI.Common import CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import ServiceRequest
################################################################################

__all__ = ("ServiceRequestEditView",)

################################################################################
class ServiceRequestEditView(View):

    def __init__(self, request: ServiceRequest):
        
        super().__init__()
        
        button_list = [
            AddRequestButton(),
            ModifyRequestButton(request.id),
            RemoveRequestButton(request.id),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class AddRequestButton(FroggeButton):

    def __init__(self):

        super().__init__(
            style=ButtonStyle.success,
            label="Add a New Request",
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
class ModifyRequestButton(FroggeButton):
    
    def __init__(self, request_id: int):
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Modify This Request",
            disabled=False,
            row=0
        )
        
        self.request_id: int = request_id
        
    async def callback(self, interaction: Interaction):
        request = self.view.ctx[self.request_id]
        await request.menu(interaction)

        await self.view.update(
            pages=await self.view.ctx.make_pages(interaction.user.id),
            current_page=self.view.current_page
        )
        
################################################################################
class RemoveRequestButton(FroggeButton):
    
    def __init__(self, request_id: int):
        
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove this Request",
            disabled=False,
            row=0
        )

        self.request_id: int = request_id
        
    async def callback(self, interaction: Interaction):
        request = self.view.ctx[self.request_id]
        await request.remove(interaction)

        await self.view.update(
            pages=await self.view.ctx.make_pages(interaction.user.id),
            current_page=self.view.current_page - 1 if self.view.current_page != 0 else 0
        )
        
################################################################################
