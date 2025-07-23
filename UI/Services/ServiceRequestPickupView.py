from __future__ import annotations

from typing import TYPE_CHECKING, Union

from discord import ButtonStyle
from discord.ui import Button, View

from Assets import BotEmojis

if TYPE_CHECKING:
    from Classes import ServiceRequest
################################################################################

__all__ = ("ServiceRequestPickupView",)

################################################################################
class ServiceRequestPickupView(View):

    def __init__(self, request: ServiceRequest):
        
        super().__init__(timeout=None)
        
        self.request: ServiceRequest = request

        if not request.is_accepted:
            self.add_item(AcceptButton(request.id))
        else:
            self.add_item(CancelButton(request))
    
################################################################################
class AcceptButton(Button):
    
    def __init__(self, request_id: int):
        
        super().__init__(
            style=ButtonStyle.success,
            label="Accept",
            disabled=False,
            row=0,
            emoji=BotEmojis.Check,
            custom_id=f"{request_id}_perm_accept"
        )
        
    async def callback(self, interaction):
        await self.view.request.accept(interaction)
        
################################################################################
class CancelButton(Button):
    
    def __init__(self, request: ServiceRequest):
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Cancel",
            disabled=False,
            row=0,
            emoji=BotEmojis.Cross,
            custom_id=f"{request.id}_perm_cancel"
        )
        
        self.user_id: int = request._candidate.id
        
    async def callback(self, interaction):
        if interaction.user.id == self.user_id:
            await self.view.request.cancel(interaction)
        else:
            await interaction.respond("You can't cancel a service request someone else has accepted.", ephemeral=True)
        
################################################################################
        
        