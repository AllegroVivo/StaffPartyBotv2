from dataclasses import dataclass
from typing import Optional
################################################################################

__all__ = ("InstructionsInfo",)

################################################################################
@dataclass
class InstructionsInfo:

    placeholder: str
    value: str
    title: Optional[str] = None

################################################################################
