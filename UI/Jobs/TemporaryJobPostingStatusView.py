from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import TemporaryJobPosting
################################################################################

__all__ = ("TemporaryJobPostingStatusView",)

################################################################################
class TemporaryJobPostingStatusView(FroggeView):

    def __init__(self, user: User, job: TemporaryJobPosting) -> None:

        super().__init__(user, job)

        button_list = [
            SetDescriptionButton(),
            SetSalaryButton(),
            SetScheduleButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################
class SetDescriptionButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Set Description",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_description(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class SetSalaryButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Set Salary",
            disabled=False,
            row=0,
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_salary(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())
        
################################################################################
class SetScheduleButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Set Start/End Time(s)",
            row=0,
            disabled=False
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_schedule(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())
        
################################################################################
