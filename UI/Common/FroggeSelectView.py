from __future__ import annotations

from typing import List

from discord import User, Interaction, SelectOption, ComponentType
from discord.ui import Select

from .FroggeView import FroggeView
from .CloseMessage import CloseMessageButton
################################################################################

__all__ = ("FroggeSelectView",)

################################################################################
class FroggeSelectView(FroggeView):

    def __init__(
        self,
        owner: User,
        options: List[SelectOption],
        multi_select: bool = False,
        return_interaction: bool = False,
        show_close: bool = True,
        select_type: ComponentType = ComponentType.string_select,
        close_text: str = "Close Message"
    ):

        super().__init__(owner, None)

        self.return_interaction = return_interaction

        self.add_item(OptionSelect(options, multi_select, select_type))
        self.add_item(CloseMessageButton(close_text)) if show_close else None

################################################################################
class OptionSelect(Select):

    def __init__(self, options: List[SelectOption], multi_select: bool, select_type: ComponentType):

        if options is not None and len(options) == 0:
            options.append(SelectOption(label="No options available", value="-1"))

        super().__init__(
            select_type=select_type,
            placeholder="Select an option...",
            options=options,
            min_values=1,
            max_values=1 if not multi_select else len(options),
            disabled=(options[0].value == "-1") if options else False,
            row=0,
        )

        self.multi_select = multi_select

    async def callback(self, interaction: Interaction):
        if not self.view.return_interaction:
            self.view.value = self.values if self.multi_select else self.values[0]
        else:
            self.view.value = (
                self.values if self.multi_select else self.values[0],
                interaction
            )
        self.view.complete = True

        if not self.view.return_interaction:
            await interaction.message.edit()
        await self.view.stop()  # type: ignore

################################################################################
