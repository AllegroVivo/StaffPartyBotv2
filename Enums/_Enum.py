from __future__ import annotations

from enum import Enum
from typing import List

from discord import SelectOption
################################################################################

__all__ = ("FroggeEnum",)

################################################################################
class FroggeEnum(Enum):

    @classmethod
    def __len__(cls) -> int:

        return sum([1 for _ in cls])

################################################################################
    @property
    def proper_name(self) -> str:

        return self.name

################################################################################
    @classmethod
    def select_options(cls) -> List[SelectOption]:

        return [x.select_option() for x in cls]

################################################################################
    def select_option(self) -> SelectOption:

        return SelectOption(label=self.proper_name, value=str(self.value))

################################################################################
    def __gt__(self, other) -> bool:

        return self.value > other.value

################################################################################
    def __lt__(self, other) -> bool:

        return self.value < other.value

################################################################################
