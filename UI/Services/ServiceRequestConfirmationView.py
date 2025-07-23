from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ButtonStyle, User, Interaction

from UI.Common import FroggeButton, FroggeView

if TYPE_CHECKING:
    from Classes import ServiceRequest
################################################################################

__all__ = ("ServiceRequestConfirmationView",)

################################################################################
class ServiceRequestConfirmationView(FroggeView):

    def __init__(self, owner: User, req: ServiceRequest):
        
        super().__init__(owner, req)
        
        button_list = [
            SetServiceTypeButton(),
            SetDescriptionButton(),
            SetBudgetButton(),
            SetDataCenterButton(),
            ConfirmRequestButton(),
            CancelRequestButton(),
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()
        
################################################################################
class SetServiceTypeButton(FroggeButton):
    
    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Service Type",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_service_type(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.confirmation_embed())
        
################################################################################
class SetDescriptionButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Description",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_description(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.confirmation_embed())

################################################################################
class SetBudgetButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Budget",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_budget(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.confirmation_embed())

################################################################################
class SetDataCenterButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Data Center",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.set_data_center(interaction)
        await self.view.edit_message_helper(interaction, embed=await self.view.ctx.confirmation_embed())

################################################################################
class ConfirmRequestButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.success,
            label="Confirm Request & Submit",
            disabled=False,
            row=1
        )

    async def callback(self, interaction: Interaction) -> None:
        self.view.complete = True
        await self.view.stop()  # type: ignore

        await self.view.ctx.submit(interaction)

################################################################################
class CancelRequestButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.danger,
            label="Cancel Request & Discard",
            disabled=False,
            row=1
        )

    async def callback(self, interaction: Interaction) -> None:
        removed = await self.view.ctx.remove(interaction)
        if removed:
            self.view.complete = True
            await self.view.stop()  # type: ignore

################################################################################
