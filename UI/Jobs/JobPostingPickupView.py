from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button, View

from Assets import BotEmojis

if TYPE_CHECKING:
    from Classes import TemporaryJobPosting
################################################################################

__all__ = ("JobPostingPickupView",)

################################################################################
class JobPostingPickupView(View):

    def __init__(self, posting: TemporaryJobPosting):
        
        super().__init__(timeout=None)
        
        self.posting: TemporaryJobPosting = posting

        if posting._candidate.id is None:
            self.add_item(AcceptButton(posting.id))
        else:
            self.add_item(CancelButton(posting))
    
################################################################################
class AcceptButton(Button):
    
    def __init__(self, posting_id: int):
        
        super().__init__(
            style=ButtonStyle.success,
            label="Accept",
            disabled=False,
            row=0,
            emoji=BotEmojis.Check,
            custom_id=f"{posting_id}_accept"
        )
        
    async def callback(self, interaction):
        await self.view.posting.candidate_accept(interaction)       
        
################################################################################
class CancelButton(Button):
    
    def __init__(self, posting: TemporaryJobPosting):
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Cancel",
            disabled=False,
            row=0,
            emoji=BotEmojis.Cross,
            custom_id=f"{posting.id}_cancel"
        )
        
        self.user_id: int = posting._candidate.id
        
    async def callback(self, interaction):
        if interaction.user.id == self.user_id:
            await self.view.posting.cancel(interaction)
        else:
            await interaction.respond("You can't cancel a job posting for someone else.", ephemeral=True)
        
################################################################################
        
        