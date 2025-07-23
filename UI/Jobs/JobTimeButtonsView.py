from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from Assets import BotEmojis
from Enums import TimeType
from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import TemporaryJobPosting
################################################################################

__all__ = ("JobTimeButtonsView",)

################################################################################
class JobTimeButtonsView(FroggeView):

    def __init__(self, user: User, job: TemporaryJobPosting) -> None:

        super().__init__(user, job)

        button_list = [
            StartTimeButton(),
            EndTimeButton(),
            BothTimesButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################
class StartTimeButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Change Start Time",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.time_menu(interaction, TimeType.StartTime)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.time_menu_status())

################################################################################
class EndTimeButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Change End Time",
            disabled=False,
            row=0,
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.time_menu(interaction, TimeType.EndTime)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.time_menu_status())

################################################################################
class BothTimesButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Change Both Times",
            disabled=False,
            row=0,
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_both_times(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.time_menu_status())

################################################################################
