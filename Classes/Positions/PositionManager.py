from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from discord import Interaction, User, Embed

from Classes.Common import ObjectManager
from UI.Common import FroggeView
from .Position import Position

if TYPE_CHECKING:
    from Classes import StaffPartyBot, Requirement
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

        self._requirements: List[Requirement] = []
    
################################################################################
    async def load_all(self, payload: Any) -> None:
        
        self._managed = [Position(self, **pos) for pos in payload["positions"]]
        self._requirements = [Requirement(self, **req) for req in payload["global_requirements"]]

################################################################################
    def finalize_load(self) -> None:

        for req in self._requirements:
            req.finalize_load()

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
