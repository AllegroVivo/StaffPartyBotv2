from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import BGCheck
################################################################################

__all__ = ("BGCheckMenuView",)

################################################################################
class BGCheckMenuView(FroggeView):

    def __init__(self, owner: User, bg_check: BGCheck) -> None:

        super().__init__(owner, bg_check)

        button_list = [
            EditNamesButton(),
            AddVenueButton(),
            RemoveVenueButton(),
            SubmitAndAgreeButton(),
            SubmitAndRejectButton(),
            CloseMessageButton(),
        ]
        
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################
class EditNamesButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Edit Names",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.names)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_names(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class AddVenueButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Add Experience",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.venues)
        self.disabled = len(self.view.ctx.venues) >= 3

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.add_venue(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class RemoveVenueButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Remove Experience",
            disabled=False,
            row=0
        )
        
    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.venues)
        self.disabled = len(self.view.ctx.venues) == 0

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.remove_venue(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class SubmitAndAgreeButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Submit and Agree",
            disabled=False,
            row=1,
            emoji=BotEmojis.ThumbsUp
        )

    async def callback(self, interaction: Interaction) -> None:
        result = await self.view.ctx.submit(interaction, True)

        if result:
            self.view.complete = True
            await self.view.stop()  # type: ignore

################################################################################
class SubmitAndRejectButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Submit and Disagree",
            disabled=False,
            row=1,
            emoji=BotEmojis.ThumbsDown
        )

    async def callback(self, interaction: Interaction) -> None:
        result = await self.view.ctx.submit(interaction, False)

        if result:
            self.view.complete = True
            await self.view.stop()  # type: ignore

################################################################################
