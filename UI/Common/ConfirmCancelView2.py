from __future__ import annotations

from typing import Union, Optional

from discord import ButtonStyle, Interaction, Member, User
from discord.ui import Button

from .FroggeView import FroggeView
################################################################################

__all__ = ("ConfirmCancelView2",)

################################################################################
class ConfirmCancelView2(FroggeView):

    def __init__(
        self,
        owner: Union[Member, User],
        return_interaction: bool = False,
        show_cancel: bool = True,
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
        confirm_style: Optional[ButtonStyle] = None,
        cancel_style: Optional[ButtonStyle] = None,
        **kwargs
    ):
        """
        Specifically returns an interaction when `return_interaction` is True,
        regardless of the button pressed.

        (Note that in the standard `ConfirmCancelView`, the interaction is only
        returned when the confirm button is pressed, and `False` is returned
        otherwise)
        """

        self.return_interaction: bool = return_interaction
        super().__init__(owner, None, **kwargs)

        self.add_item(ConfirmCancelButton(confirm_text, confirm_style, 1))
        if show_cancel:
            self.add_item(ConfirmCancelButton(cancel_text, cancel_style, 2))

################################################################################
class ConfirmCancelButton(Button):

    def __init__(self, text: str, style: Optional[ButtonStyle], button_type: int):

        super().__init__(
            style=style or (
                ButtonStyle.success
                if button_type == 1
                else ButtonStyle.danger
            ),
            label=text,
            disabled=False,
            row=0
        )

        self._type: int = button_type

    async def callback(self, interaction: Interaction):
        result = self._type == 1
        self.view.value = (
            result if not self.view.return_interaction
            else (result, interaction)
        )
        self.view.complete = True

        if self._type == 1 and not self.view.return_interaction:
            await self.view.dummy_response(interaction)
        await self.view.stop()  # type: ignore

################################################################################
