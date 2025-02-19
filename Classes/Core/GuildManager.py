from __future__ import annotations

from discord import Guild
from typing import TYPE_CHECKING, List

from .GuildData import GuildData

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("GuildManager",)

################################################################################
class GuildManager:

    __slots__ = (
        "_state",
        "_fguilds"
    )

################################################################################
    def __init__(self, bot: StaffPartyBot):

        self._state: StaffPartyBot = bot
        self._fguilds: List[GuildData] = []

################################################################################
    def __getitem__(self, guild_id: int) -> GuildData:

        for frogge in self._fguilds:
            if frogge.guild_id == guild_id:
                return frogge

################################################################################
    def __iter__(self):

        return iter(self._fguilds)

################################################################################
    def __contains__(self, guild: Guild) -> bool:

        return guild in [fguild.parent for fguild in self._fguilds]

################################################################################
    @property
    def fguilds(self) -> List[GuildData]:

        return self._fguilds

################################################################################
    async def init_guild(self, guild: Guild, register_commands: bool = False) -> GuildData:

        frogge_guild = GuildData(self._state, guild)
        self._fguilds.append(frogge_guild)

        if register_commands:
            await self._state.register_commands(force=True, guild_id=guild.id)

        return frogge_guild

################################################################################
