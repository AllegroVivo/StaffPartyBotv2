from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, Embed

from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import (
        Venue,
        StaffPartyBot,
        JobPostingManager,
        TemporaryJobPosting,
        PermanentJobPosting
    )
################################################################################

__all__ = ("VenueJobSupervisor", )

################################################################################
class VenueJobSupervisor:

    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Venue) -> None:

        self._parent: Venue = parent

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._parent.bot

################################################################################
    @property
    def jobs_manager(self) -> JobPostingManager:

        return self.bot.jobs_manager

################################################################################
    @property
    def temp_jobs(self) -> List[TemporaryJobPosting]:

        return [
            j
            for j in self.jobs_manager.temporary_postings
            if j._venue_id == self._parent.id
        ]

################################################################################
    @property
    def perm_jobs(self) -> List[PermanentJobPosting]:

        return [
            j
            for j in self.jobs_manager.permanent_postings
            if j._venue_id == self._parent.id
        ]

################################################################################
    def status(self) -> Embed:

        return U.make_embed(
            title=f"Jobs Menu for {self._parent.name}",
            description=(
                "\n".join([f"- {j.format()}" for j in self.temp_jobs])
                if self.temp_jobs else "`No temporary jobs available.`"
            )
        )

################################################################################
    async def menu(self, interaction: Interaction) -> None:

        await self._parent.temp_job_wizard(interaction)

        embed = self.status()
        await interaction.respond(embed=embed)

################################################################################
