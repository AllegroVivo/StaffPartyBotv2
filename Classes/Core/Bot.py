from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("StaffPartyBot", )

################################################################################
class StaffPartyBot:

    __slots__ = (
        "_guild_mgr",
        "_img_dump",
        "_db",
        "_venues_client",
        "_report_mgr",
    )

################################################################################
    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self._img_dump: TextChannel = None  # type: ignore

        self._guild_mgr: GuildManager = GuildManager(self)
        self._db: Database = Database(self)
        self._venues_client: XIVVenuesClient = XIVVenuesClient(self)
        self._report_mgr: ReportManager = ReportManager(self)

################################################################################
