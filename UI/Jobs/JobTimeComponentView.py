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

__all__ = ("JobTimeComponentView",)

################################################################################
class JobTimeComponentView(FroggeView):

    def __init__(self, user: User, job: TemporaryJobPosting, t_type: TimeType) -> None:

        super().__init__(user, job)

        self.time_type: TimeType = t_type

        button_list = [
            ChangeYearButton(),
            ChangeMonthButton(),
            ChangeDayButton(),
            ChangeHourButton(),
            ChangeMinuteButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################
class ChangeYearButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Year",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_year(interaction, self.view.time_type)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.time_status(self.view.time_type))

################################################################################
class ChangeMonthButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Month",
            disabled=False,
            row=0,
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_month(interaction, self.view.time_type)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.time_status(self.view.time_type))

################################################################################
class ChangeDayButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Day",
            disabled=False,
            row=0,
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_day(interaction, self.view.time_type)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.time_status(self.view.time_type))

################################################################################
class ChangeHourButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Hour",
            disabled=False,
            row=0,
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_hour(interaction, self.view.time_type)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.time_status(self.view.time_type))

################################################################################
class ChangeMinuteButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Minute",
            disabled=False,
            row=0,
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_minute(interaction, self.view.time_type)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.time_status(self.view.time_type))

################################################################################
