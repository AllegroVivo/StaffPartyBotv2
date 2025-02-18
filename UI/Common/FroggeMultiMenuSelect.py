from __future__ import annotations

from typing import List, Any

from discord import User, Interaction, SelectOption
from discord.ui import Select

from .FroggeView import FroggeView
from .CloseMessage import CloseMessageButton
################################################################################

__all__ = ("FroggeMultiMenuSelect",)

################################################################################
class FroggeMultiMenuSelect(FroggeView):

    def __init__(self,  owner: User, options: List[SelectOption], chunk_size: int = 20):

        super().__init__(owner, None)

        chunked_options = [options[i:i + chunk_size] for i in range(0, len(options), chunk_size)]

        for idx, opts in enumerate(chunked_options):
            self.add_item(ItemSelect(opts, idx))
        self.add_item(CloseMessageButton())

################################################################################
class ItemSelect(Select):

    def __init__(self, options: List[SelectOption], row: int):

        if not options:
            options.append(SelectOption(label="No options available", value="-1"))

        super().__init__(
            placeholder="Select an item..." if row == 0 else " ",
            options=options,
            disabled=options[0].value == "-1",
            row=row,
        )

    async def callback(self, interaction: Interaction):
        self.view.value = self.values[0]
        self.view.complete = True

        await interaction.message.edit()
        await self.view.stop()  # type: ignore

################################################################################
