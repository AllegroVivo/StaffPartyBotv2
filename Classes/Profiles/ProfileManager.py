from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from discord import Interaction, User, Embed, ForumChannel, Member, Thread

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
    @property
    def profiles(self) -> List[Profile]:

        return self._managed

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
    def get_profile(self, user_id: int) -> Profile:

        for p in self._managed:
            if p.user_id == user_id:
                return p

        profile = Profile.new(self, user_id)
        self._managed.append(profile)

        return profile

################################################################################
    async def user_menu(self, interaction: Interaction) -> None:

        profile = self.get_profile(interaction.user.id)
        await profile.menu(interaction)

################################################################################
    async def on_member_leave(self, member: Member) -> bool:

        for profile in self._managed:
            if profile.user_id == member.id:
                post_message = await profile.post_message
                try:
                    if isinstance(post_message.channel, Thread):
                        await post_message.channel.delete()
                    else:
                        await post_message.delete()
                    return True
                except:
                    pass

        return False

################################################################################
