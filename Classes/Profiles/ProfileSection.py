from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from Assets import BotEmojis

if TYPE_CHECKING:
    from Classes import Profile, StaffPartyBot
################################################################################

__all__ = ("ProfileSection",)

################################################################################
class ProfileSection:
    
    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Profile) -> None:
        
        self._parent: Profile = parent
        
################################################################################
    @property
    def bot(self) -> StaffPartyBot:
        
        return self._parent.bot
    
################################################################################
    @property
    def parent(self) -> Profile:
        
        return self._parent
    
################################################################################
    @property
    def profile_id(self) -> int:
        
        return self._parent.id
    
################################################################################
    @staticmethod
    def progress_emoji(attribute: Optional[Any]) -> str:

        return str(BotEmojis.Cross if not attribute else BotEmojis.Check)

################################################################################
