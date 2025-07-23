from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from discord import Interaction, ButtonStyle
from discord.ui import View

from Assets import BotEmojis
from UI.Common import FroggeButton

if TYPE_CHECKING:
    from Classes import Profile, DJProfile
################################################################################

__all__ = ("ProfileUserMuteView",)

################################################################################        
class ProfileUserMuteView(View):

    def __init__(self, profile: Union[Profile, DJProfile]):

        super().__init__(timeout=None)

        self.profile: Union[Profile, DJProfile] = profile
        self.add_item(MuteUserButton(self.profile.id, self.profile.user_id))

################################################################################        
class MuteUserButton(FroggeButton):

    def __init__(self, _id: int, user_id: int) -> None:

        super().__init__(
            style=ButtonStyle.secondary,
            label="Mute/Unmute User",
            disabled=False,
            row=0,
            custom_id=f"mute_user_{_id}",
            emoji=BotEmojis.Mute
        )

        self.user_id: int = user_id

    async def callback(self, interaction: Interaction) -> None:
        await interaction.client.venue_manager.mute_user(interaction, self.user_id)  # type: ignore

################################################################################
