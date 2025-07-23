from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle

from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import ServiceRequest
################################################################################

__all__ = ("ServiceRequestStatusView",)

################################################################################        
class ServiceRequestStatusView(FroggeView):

    def __init__(self, user: User, request: ServiceRequest):

        super().__init__(user, request)

        button_list = [
            SetDescriptionButton(),
            SetBudgetButton(),
            SetDataCenterButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################
class SetDescriptionButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            label="Description",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.description)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_description(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class SetBudgetButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            label="Budget",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.budget)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_budget(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
class SetDataCenterButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            label="Data Center",
            disabled=False,
            row=0
        )

    def set_attributes(self) -> None:
        self.set_style(self.view.ctx.data_center)

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_data_center(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.status())

################################################################################
