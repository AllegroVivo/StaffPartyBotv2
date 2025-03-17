from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button, View

from Assets import BotEmojis

if TYPE_CHECKING:
    from Classes import TraineeMessage
################################################################################

__all__ = ("TraineeMessagePickupView",)

################################################################################
class TraineeMessagePickupView(View):

    def __init__(self, t_msg: TraineeMessage):
        
        super().__init__(timeout=None)
        
        self.ctx: TraineeMessage = t_msg
        self.add_item(PickupTraineeButton(t_msg.bot.SPB_ID))
    
################################################################################
class PickupTraineeButton(Button):
    
    def __init__(self, spb_id: int):
        
        super().__init__(
            style=ButtonStyle.success,
            label="Pickup Trainee",
            disabled=False,
            row=0,
            emoji=BotEmojis.Spaceship,
            custom_id=f"{spb_id}_trainee_pickup"
        )
        
    async def callback(self, interaction):
        await self.view.posting.pickup_trainee(interaction)
        
################################################################################
        