from __future__ import annotations

from typing import TYPE_CHECKING, Any

from discord import Interaction, User, Embed

from Classes.Common import ObjectManager
from UI.Common import FroggeView

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("PositionManager", )

################################################################################
class PositionManager(ObjectManager):

    __slots__ = (
        "_requirements",
    )
    
################################################################################
    def __init__(self, state: StaffPartyBot) -> None:

        super().__init__(state)
    
################################################################################
    async def load_all(self, payload: Any) -> None:
        
        pass

################################################################################
    async def status(self) -> Embed:
        
        pass

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:
        
        pass

################################################################################
    async def add_item(self, interaction: Interaction) -> None:
        
        pass

################################################################################
    async def modify_item(self, interaction: Interaction) -> None:
        
        pass

################################################################################
    async def remove_item(self, interaction: Interaction) -> None:
        
        pass
    
################################################################################