from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional, Dict

from discord import Embed, Interaction, User

from Assets import BotEmojis

if TYPE_CHECKING:
    from Classes import Profile, StaffPartyBot
    from UI.Common import FroggeView
################################################################################

__all__ = ("ProfileSection",)

################################################################################
class ProfileSection(ABC):
    
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
    @property
    def user_id(self) -> int:

        return self._parent.user_id

################################################################################
    @staticmethod
    def progress_emoji(attribute: Optional[Any]) -> str:

        return str(BotEmojis.Cross if not attribute else BotEmojis.Check)

################################################################################
    def update(self) -> None:

        self.bot.db.update.profile(self)

################################################################################
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:

        raise NotImplementedError

################################################################################
    @abstractmethod
    def status(self) -> Embed:

        raise NotImplementedError

################################################################################
    @abstractmethod
    def get_menu_view(self, user: User) -> FroggeView:

        raise NotImplementedError

################################################################################
    @abstractmethod
    def compile(self) -> Any:

        raise NotImplementedError

################################################################################
    @abstractmethod
    def progress(self) -> str:

        raise NotImplementedError

################################################################################
    async def menu(self, interaction: Interaction) -> None:

        embed = self.status()
        view = self.get_menu_view(interaction.user)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    async def update_post_components(self, update_embeds: bool = True, update_view: bool = True) -> bool:

        return await self._parent.update_post_components(update_embeds, update_view)

################################################################################
