from __future__ import annotations

import re

from typing import TYPE_CHECKING, Optional, Union

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from .FroggeModal import FroggeModal
from Utilities.ErrorMessage import ErrorMessage

if TYPE_CHECKING:
    from .InstructionsInfo import InstructionsInfo
################################################################################

__all__ = ("BasicNumberModal",)

################################################################################
class BasicNumberModal(FroggeModal):

    def __init__(
        self,
        title: str,
        attribute: str,
        cur_val: Optional[Union[int, float]] = None,
        example: Optional[str] = None,
        min_length: int = 1,
        max_length: int = 3,
        required: bool = True,
        instructions: Optional[InstructionsInfo] = None,
        return_interaction: bool = False,
        _number_cls: type = int
    ):

        super().__init__(title=title)

        if instructions is not None:
            self.add_item(
                InputText(
                    style=InputTextStyle.multiline,
                    label="Instructions",
                    placeholder=instructions.placeholder,
                    value=instructions.value,
                    required=False
                )
            )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label=attribute,
                placeholder=example,
                value=str(cur_val) if cur_val is not None else None,
                min_length=min_length,
                max_length=max_length,
                required=required
            )
        )

        self.return_interaction: bool = return_interaction
        self._number_cls: type = _number_cls

    async def callback(self, interaction: Interaction):
        raw_value = (
            (self.children[1].value or None)
            if len(self.children) == 2
            else (self.children[0].value or None)
        )

        if self._number_cls is float:
            parsed = self._evaluate_float(raw_value)
        else:
            parsed = self._parse_salary(raw_value)

        if parsed is None:
            error = InvalidNumber(raw_value, self._number_cls)
            await interaction.respond(embed=error, ephemeral=True)
            return

        if self.return_interaction:
            self.value = parsed, interaction
        else:
            self.value = parsed
            await self.dummy_response(interaction)

        self.complete = True
        self.stop()

################################################################################
    @staticmethod
    def _parse_salary(salary: str) -> Optional[int]:

        # Remove commas and whitespace, and make lowercase
        salary = salary.lower().strip().replace(",", "")

        try:
            if salary.endswith("k"):
                return int(float(salary[:-1]) * 1000)
            elif salary.endswith("m"):
                return int(float(salary[:-1]) * 1000000)
            else:
                return int(float(salary))
        except ValueError:
            return None

###############################################################################
    @staticmethod
    def _evaluate_float(expr: str) -> Optional[float]:
        """
        Evaluate an input string as either a float or a fraction (division).
        Supports only division (e.g., "1/16") or a direct float (e.g., "0.0625").

        Args:
            expr (str): The input string to evaluate.

        Returns:
            float: The evaluated float value.
        """

        # Allow only digits, "/", ".", and optional whitespace
        if not re.match(r"^\s*\d+(\.\d+)?\s*(/\s*\d+(\.\d+)?)?\s*$", expr):
            return None

        try:
            # If "/" is present, evaluate as a fraction
            if "/" in expr:
                numerator, denominator = map(float, expr.split("/"))
                if denominator == 0:
                    raise ValueError("Division by zero is not allowed.")
                return numerator / denominator
            else:
                # Otherwise, parse as a float
                return float(expr)
        except (ValueError, ZeroDivisionError):
            return None

################################################################################
class InvalidNumber(ErrorMessage):

    def __init__(self, value: str, _number_cls: type):
        super().__init__(
            title="Invalid Number",
            description=f"Invalid Value: {value}",
            message="The numerical value you entered is invalid.",
            solution=(
                "Enter a decimal number or a fraction."
                if _number_cls is float
                else "Enter a whole number."
            )
        )

################################################################################
