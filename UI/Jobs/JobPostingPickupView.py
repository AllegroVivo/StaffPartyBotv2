from __future__ import annotations

from typing import TYPE_CHECKING, Union

from discord import ButtonStyle
from discord.ui import Button, View

from Assets import BotEmojis

if TYPE_CHECKING:
    from Classes import TemporaryJobPosting, PermanentJobPosting
################################################################################

__all__ = ("JobPostingPickupView",)

################################################################################
class JobPostingPickupView(View):

    def __init__(self, posting: Union[TemporaryJobPosting, PermanentJobPosting]):
        
        super().__init__(timeout=None)
        
        self.posting: Union[TemporaryJobPosting, PermanentJobPosting] = posting

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
            custom_id=f"{posting_id}_perm_accept"
        )
        
    async def callback(self, interaction):
        await self.view.posting.candidate_accept(interaction)       
        
################################################################################
class CancelButton(Button):
    
    def __init__(self, posting: Union[TemporaryJobPosting, PermanentJobPosting]):
        
        super().__init__(
            style=ButtonStyle.secondary,
            label="Cancel",
            disabled=False,
            row=0,
            emoji=BotEmojis.Cross,
            custom_id=f"{posting.id}_perm_cancel"
        )
        
        self.user_id: int = posting._candidate.id
        
    async def callback(self, interaction):
        if interaction.user.id == self.user_id:
            await self.view.posting.cancel(interaction)
        else:
            await interaction.respond("You can't cancel a job posting someone else has accepted.", ephemeral=True)
        
################################################################################
        
        