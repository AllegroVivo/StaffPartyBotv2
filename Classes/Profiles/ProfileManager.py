from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

from discord import Interaction, User, Embed

from Classes.Common import ObjectManager

if TYPE_CHECKING:
    from Classes import StaffPartyBot
    from UI.Common import FroggeView
################################################################################

__all__ = ("ProfileManager", )

################################################################################
class ProfileManager(ObjectManager):

    def __init__(self, state: StaffPartyBot) -> None:

        super().__init__(state)

################################################################################
    async def load_all(self, payload: List[Dict[str, Any]]) -> None:

        self._managed = [Profile(self, **p) for p in payload]

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
