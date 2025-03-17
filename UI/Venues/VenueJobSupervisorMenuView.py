from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import VenueJobSupervisor, VenueTag
################################################################################

__all__ = ("VenueJobSupervisorMenuView",)

################################################################################
class VenueJobSupervisorMenuView(FroggeView):

    def __init__(self, user: User, ctx: VenueJobSupervisor) -> None:

        super().__init__(user, ctx)

        button_list = [
            AddTemporaryJobButton(),
            ModifyTemporaryJobButton(),
            RemoveTemporaryJobButton(),
            AddPermanentJobButton(),
            ModifyPermanentJobButton(),
            RemovePermanentJobButton(),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

        self.set_button_attributes()

################################################################################
class AddTemporaryJobButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.success,
            label="Post Temporary Job",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.add_temp_job(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class ModifyTemporaryJobButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.primary,
            label="Modify Temporary Job",
            disabled=False,
            row=0,
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.modify_temp_job(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class RemoveTemporaryJobButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Temporary Job",
            row=0,
            disabled=False
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.remove_temp_job(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class AddPermanentJobButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.success,
            label="Post Permanent Job",
            row=1,
            disabled=False
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.add_perm_job(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())

################################################################################
class ModifyPermanentJobButton(FroggeButton):

    def __init__(self) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label="Modify Permanent Job",
            row=1,
            disabled=False
        )

    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.modify_perm_job(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
class RemovePermanentJobButton(FroggeButton):
    
    def __init__(self) -> None:
        
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Permanent Job",
            row=1,
            disabled=False
        )
        
    async def callback(self, interaction: Interaction) -> None:
        await self.view.ctx.remove_perm_job(interaction)
        await self.view.edit_message_helper(interaction, embed=self.view.ctx.status())
        
################################################################################
