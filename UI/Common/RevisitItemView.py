from __future__ import annotations

from typing import TypeVar

from discord import Interaction, ButtonStyle

from Assets import BotEmojis
from UI.Common import FroggeView, FroggeButton
################################################################################

__all__ = ("RevisitItemView",)

T = TypeVar("T")

################################################################################
class RevisitItemView(FroggeView):

    def __init__(self, context: T) -> None:

        super().__init__(None, context)

        button_list = [
            ClosePostingButton(),
            ReOpenPostingButton(),
            MoreTimeButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################
class ClosePostingButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.success,
            label="Candidate Worked Out, Close Posting",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.remove(interaction)
        await self.view.stop()  # type: ignore
        await interaction.respond(
            "The job posting has been closed and the candidate has been marked as hired.",
            ephemeral=True
        )

################################################################################
class ReOpenPostingButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Candidate Did Not Work Out, Re-Open Posting",
            disabled=False,
            row=0,
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.cancel(None)
        await self.view.stop()  # type: ignore
        await interaction.respond(
            "The job posting has been re-opened and the candidate has been marked as not hired.",
            ephemeral=True
        )
        
################################################################################
class MoreTimeButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="I Need More Time, Ask Me Later",
            disabled=False,
            emoji=BotEmojis.Clock,
            row=1,
        )

    async def callback(self, interaction: Interaction) -> None:
        self.view.ctx.register_revisit_timer()
        await self.view.stop()  # type: ignore
        await interaction.respond(
            "The job posting will be revisited later. You can close it or re-open it at that time.",
            ephemeral=True
        )

################################################################################
