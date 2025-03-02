from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from discord import Interaction, User, Embed, ForumChannel

from Classes.Common import ObjectManager
from .Profile import Profile

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
    async def load_all(self, payload: Dict[str, Any]) -> None:

        self._managed = [Profile(self, **p) for p in payload["profiles"]]

################################################################################
    @property
    async def post_channel(self) -> Optional[ForumChannel]:

        return await self.bot.channel_manager.profiles_channel

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
