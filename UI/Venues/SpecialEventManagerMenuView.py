from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import SpecialEventManager, VenueTag
################################################################################

__all__ = ("SpecialEventManagerMenuView",)

################################################################################
class SpecialEventManagerMenuView(FroggeView):

    def __init__(self, user: User, ctx: SpecialEventManager) -> None:

        super().__init__(user, ctx)

        button_list = [
            AddEventButton(),
            ModifyEventButton(),
            RemoveEventButton(),
            ToggleParticipationButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################
class AddEventButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.success,
            label="Add New Event",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.add_event(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class ModifyEventButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Modify Special Event",
            disabled=False,
            row=0,
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.modify_event(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class RemoveEventButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.danger,
            label="Remove/Cancel Event",
            row=0,
            disabled=False
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.remove_event(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class ToggleParticipationButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            row=1,
            disabled=False
        )

    def set_attributes(self) -> None:
        self.label = (
            "I Want to Receive Event Participation Pings"
            if self.view.ctx.event_participation
            else "I Do Not Want Event Participation Pings"
        )
        self.style = (
            ButtonStyle.success
            if self.view.ctx.event_participation
            else ButtonStyle.primary
        )
        self.emoji = (
            BotEmojis.ThumbsUp
            if self.view.ctx.event_participation
            else BotEmojis.ThumbsDown
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.toggle_participation(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
