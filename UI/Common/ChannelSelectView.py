from __future__ import annotations

from typing import List

from discord import User, Interaction, SelectOption, ComponentType, ChannelType
from discord.ui import Select

from .FroggeView import FroggeView
from .CloseMessage import CloseMessageButton
################################################################################

__all__ = ("ChannelSelectView",)

################################################################################
class ChannelSelectView(FroggeView):

    def __init__(
        self,
        owner: User,
        restrictions: List[ChannelType] = None,
    ):

        super().__init__(owner, None)

        self.add_item(OptionSelect(restrictions or [ChannelType.text]))
        self.add_item(CloseMessageButton())

################################################################################
class OptionSelect(Select):

    def __init__(self, restrictions: List[ChannelType]):

        super().__init__(
            ComponentType.channel_select,
            placeholder="Select an option...",
            min_values=1,
            max_values=1,
            disabled=False,
            row=0,
            channel_types=restrictions
        )

    async def callback(self, interaction: Interaction):
        self.view.value = self.values[0]
        self.view.complete = True

        await interaction.message.edit()
        await self.view.stop()  # type: ignore

################################################################################
