from dataclasses import dataclass
from typing import Optional
################################################################################

__all__ = ("InstructionsInfo",)

################################################################################
@dataclass
class InstructionsInfo:

    title: Optional[str]
    placeholder: str
    value: str

################################################################################
