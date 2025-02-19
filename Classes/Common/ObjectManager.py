from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Any, Optional

from discord import Embed, Interaction, User

if TYPE_CHECKING:
    from Classes import GuildData, StaffPartyBot, ManagedObject
    from UI.Common import FroggeView
################################################################################

__all__ = ("ObjectManager",)

################################################################################
class ObjectManager(ABC):

    __slots__ = (
        "_state",
        "_managed",
    )

    MAX_ITEMS = 80

################################################################################
    def __init__(self, state: StaffPartyBot) -> None:

        self._state: StaffPartyBot = state
        self._managed: List[ManagedObject] = []

################################################################################
    @abstractmethod
    async def load_all(self, payload: Any) -> None:

        raise NotImplementedError

################################################################################
    def __len__(self) -> int:

        return len(self._managed)

################################################################################
    def __getitem__(self, item_id: int) -> Optional[ManagedObject]:

        return next((i for i in self._managed if i.id == int(item_id)), None)

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._state

################################################################################
    @abstractmethod
    async def status(self) -> Embed:

        raise NotImplementedError

################################################################################
    @abstractmethod
    def get_menu_view(self, user: User) -> FroggeView:

        raise NotImplementedError

################################################################################
    async def main_menu(self, interaction: Interaction) -> None:

        embed = await self.status()
        view = self.get_menu_view(interaction.user)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    @abstractmethod
    async def add_item(self, interaction: Interaction) -> None:

        raise NotImplementedError

################################################################################
    @abstractmethod
    async def modify_item(self, interaction: Interaction) -> None:

        raise NotImplementedError

################################################################################
    @abstractmethod
    async def remove_item(self, interaction: Interaction) -> None:

        raise NotImplementedError

################################################################################
