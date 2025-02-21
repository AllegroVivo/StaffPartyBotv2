from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, Optional

from discord import Embed, Message, TextChannel, Interaction, ChannelType, User
from discord.abc import GuildChannel

from Classes.Common import LazyUser, LazyChannel
from Errors import InvalidChannelType
from UI.Common import CloseMessageView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import *
################################################################################

__all__ = ("SPBLogger", )

################################################################################
class SPBLogger:

    __slots__ = (
        "_state",
        "_alyah",
        "_channel",
    )

################################################################################
    def __init__(self, state: StaffPartyBot) -> None:

        self._state: StaffPartyBot = state

        self._alyah: User = None  # type: ignore
        self._channel: LazyChannel = LazyChannel(self, None)

################################################################################
    async def load_all(self, data: Dict[str, Any]) -> None:

        self._alyah = await self.bot.fetch_user(334530475479531520)
        self._channel = LazyChannel(self, data.get("log_channel_id"))

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._state

################################################################################
    @property
    async def log_channel(self) -> Optional[TextChannel]:

        return await self._channel.get()

    @log_channel.setter
    def log_channel(self, value: Optional[TextChannel]) -> None:

        self._channel.set(value)

################################################################################
    def update(self) -> None:

        self.bot.db.update.top_level(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "log_channel_id": self._channel.id,
        }

################################################################################
    async def set_log_channel(self, interaction: Interaction, channel: GuildChannel) -> None:

        if not isinstance(channel, TextChannel):
            error = InvalidChannelType(channel, "Text")
            await interaction.respond(embed=error, ephemeral=True)
            return

        self.log_channel = channel

        confirm = U.make_embed(
            title="Log Channel Set",
            description=f"Log channel has been set to {channel.mention}",
        )
        view = CloseMessageView(interaction.user)

        await interaction.respond(embed=confirm, view=view)
        await view.wait()

################################################################################
    async def _log(self, message: Embed, **kwargs) -> Optional[Message]:

        channel = await self.log_channel
        if channel is None:
            return None

        return await channel.send(embed=message, **kwargs)

################################################################################
    async def venue_created(self, venue: Venue) -> None:

        users = "\n".join(
            [f"* {u.mention} ({u.display_name})"
             for u in await venue.managers]
        )

        embed = U.make_embed(
            title="Venue Created!",
            description=(
                f"New venue `{venue.name}` has been created!\n\n"

                f"__Managers:__\n"
                f"{users}"

            ),
            timestamp=True
        )

        await self._log(embed)
        if not self.bot.DEBUG:
            await self._alyah.send(embed=embed)

################################################################################
