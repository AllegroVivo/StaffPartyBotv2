from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ButtonStyle, User, Interaction

from UI.Common import FroggeButton, FroggeView

if TYPE_CHECKING:
    from Classes import ServiceRequest
################################################################################

__all__ = ("ServiceRequestAcceptView",)

################################################################################
class ServiceRequestAcceptView(FroggeView):

    def __init__(self, req: ServiceRequest):
        
        super().__init__(None, req, timeout=2592000)  # 30-days timeout
        
        button_list = [
            AcceptRequestButton(),
            DeclineRequestButton(),
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()
        
################################################################################
class AcceptRequestButton(FroggeButton):
    
    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.success,
            label="Accept",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.accept(interaction)
        
################################################################################
class DeclineRequestButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.danger,
            label="Decline",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.decline(interaction)

################################################################################
