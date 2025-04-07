from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Dict, List

from discord import Interaction, User, Embed, ForumChannel

from Classes.Common import ObjectManager
from .DJProfile import DJProfile

if TYPE_CHECKING:
    from Classes import StaffPartyBot
    from UI.Common import FroggeView
################################################################################

__all__ = ("DJManager",)

################################################################################
class DJManager(ObjectManager):

    def __init__(self, state: StaffPartyBot) -> None:

        super().__init__(state)

################################################################################
    async def load_all(self, payload: Dict[str, Any]) -> None:

        self._managed = [DJProfile(self, **profile) for profile in payload["profiles"]]

################################################################################
    async def finalize_load(self) -> None:

        for profile in self.profiles:
            await profile.update_post_components()

################################################################################
    def __getitem__(self, user_id: int) -> Optional[DJProfile]:

        return next((profile for profile in self._managed if profile.id == int(user_id)), None)

################################################################################
    @property
    def profiles(self) -> List[DJProfile]:

        return self._managed

################################################################################
    @property
    async def post_channel(self) -> Optional[ForumChannel]:

        return await self.bot.channel_manager.dj_profiles_channel

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
    def get_profile(self, user_id: int) -> DJProfile:

        for p in self._managed:
            if p.id == int(user_id):
                return p

        profile = DJProfile.new(self, user_id)
        self._managed.append(profile)

        return profile

################################################################################
    async def user_menu(self, interaction: Interaction) -> None:

        profile = self.get_profile(interaction.user.id)
        await profile.menu(interaction)

################################################################################
