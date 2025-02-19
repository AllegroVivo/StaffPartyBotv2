from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Guild

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("GuildData", )

################################################################################
class GuildData:

    __slots__ = (
        "_state",
        "_parent"
    )

################################################################################
    def __init__(self, bot: StaffPartyBot, parent: Guild) -> None:

        self._state: StaffPartyBot = bot
        self._parent: Guild = parent

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._state

################################################################################
    @property
    def parent(self) -> Guild:

        return self._parent

################################################################################
    @property
    def guild_id(self) -> int:

        return self._parent.id

################################################################################
    @property
    def name(self) -> str:

        return self._parent.name

################################################################################
