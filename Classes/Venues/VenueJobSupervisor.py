from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, List, Literal, Union, Optional

from discord import Interaction, Embed, SelectOption

from Errors import MaxItemsReached
from UI.Common import FroggeSelectView, ConfirmCancelView
from UI.Venues import VenueJobSupervisorMenuView
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

        return sorted([
            j
            for j in self.jobs_manager.temporary_postings
            if j._venue_id == self._parent.id
        ], key=lambda j: (j.position.proper_name, j._start))

    def get_temp_job(self, job_id: int) -> Optional[TemporaryJobPosting]:

        return next((j for j in self.temp_jobs if j.id == int(job_id)), None)

################################################################################
    @property
    def perm_jobs(self) -> List[PermanentJobPosting]:

        return sorted([
            j
            for j in self.jobs_manager.permanent_postings
            if j._venue_id == self._parent.id
        ], key=lambda j: j.position.proper_name)

    def get_perm_job(self, job_id: int) -> Optional[PermanentJobPosting]:

        return next((j for j in self.perm_jobs if j.id == int(job_id)), None)

################################################################################
    def status(self) -> Embed:

        temp_counts = Counter(j.position.proper_name for j in self.temp_jobs)
        temp_pos_seen = {}  # tracks how many times we've labeled a given position
        temp_job_strs = []

        for j in self.temp_jobs:
            pos = j.position.proper_name  # or j.position.name if it's an enum/object
            if temp_counts[pos] == 1:
                # Only one job with this position -> just "Bartender"
                job_name = str(pos)
            else:
                # Multiple jobs -> "Bartender 1", "Bartender 2", ...
                temp_pos_seen[pos] = temp_pos_seen.get(pos, 0) + 1
                job_name = f"{pos} {temp_pos_seen[pos]}"

            temp_job_strs.append(j.format(job_name, False))

        temp_str = "\n".join(temp_job_strs) or "`No jobs posted.`"

        counts = Counter(j.position.proper_name for j in self.perm_jobs)
        perm_job_strs = []

        for position_name, count in counts.items():
            perm_job_strs.append(f"**{count}x {position_name}**")

        perm_str = "\n".join(perm_job_strs) or "`No jobs posted.`"

        return U.make_embed(
            title=f"Jobs Menu for {self._parent.name}",
            description=(
                "__Temporary Jobs__\n"
                f"{temp_str}\n\n"
                
                "__Permanent Jobs__\n"
                f"{perm_str}"
            )
        )

################################################################################
    async def menu(self, interaction: Interaction) -> None:

        embed = self.status()
        view = VenueJobSupervisorMenuView(interaction.user, self)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    async def add_temp_job(self, interaction: Interaction) -> None:

        if len(self.temp_jobs) >= self.bot.MAX_SELECT_OPTIONS:
            error = MaxItemsReached("Temporary Jobs", self.bot.MAX_SELECT_OPTIONS)
            await interaction.respond(embed=error, ephemeral=True)
            return

        await self.jobs_manager.temp_job_wizard(interaction, self._parent)

################################################################################
    async def _select_job(
        self,
        interaction: Interaction,
        _type: Literal["Temporary", "Permanent"],
        op: Literal["Modify", "Remove"]
    ) -> Optional[Union[TemporaryJobPosting, PermanentJobPosting]]:

        jobs = self.temp_jobs if _type == "Temporary" else self.perm_jobs
        pos_counts = Counter(j.position.proper_name for j in jobs)
        position_seen = {}  # tracks how many times we've labeled a given position
        options = []

        for j in jobs:
            pos = j.position.proper_name  # or j.position.name if it's an enum/object
            if pos_counts[pos] == 1:
                # Only one job with this position -> just "Bartender"
                label = str(pos)
            else:
                # Multiple jobs -> "Bartender 1", "Bartender 2", ...
                position_seen[pos] = position_seen.get(pos, 0) + 1
                label = f"{pos} {position_seen[pos]}"

            has_tz = hasattr(j, "timezone")
            if has_tz:
                if j.timezone is not None:
                    await j.get_tz(interaction)
                assert j.timezone is not None, (
                    f"Job {j.id} ({j.position.proper_name}) has no timezone set."
                )

            options.append(
                SelectOption(
                    label=label,
                    value=str(j.id),
                    description=(
                        j.start_time.astimezone(j.timezone).strftime("%A, %B %d, %Y %I:%M %p")
                        if has_tz
                        else None
                    )
                )
            )

        prompt = U.make_embed(
            title=f"Select {_type} Job",
            description=(
                f"Please select the job you wish to {op.lower()} from the "
                f"list below."
            )
        )
        view = FroggeSelectView(interaction.user, options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return None

        if _type == "Temporary":
            return self.get_temp_job(view.value)
        else:
            return self.get_perm_job(view.value)

################################################################################
    async def modify_temp_job(self, interaction: Interaction) -> None:

        job = await self._select_job(interaction, "Temporary", "Modify")
        if job is None:
            return

        # If the job is already accepted, we can show and error and return.
        if job.is_accepted:
            error = U.make_embed(
                title="Job Already Accepted",
                description=(
                    "This job has already been accepted by a candidate.\n\n"
                    
                    "If you need to make changes, please cancel the job posting\n"
                    "and create a new one.\n\n"
                    
                    "The candidate will be notified of the cancellation."
                )
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        await job.menu(interaction)

################################################################################
    async def remove_temp_job(self, interaction: Interaction) -> None:

        job = await self._select_job(interaction, "Temporary", "Remove")
        if job is None:
            return

        await job.remove(interaction)

################################################################################
    async def add_perm_job(self, interaction: Interaction) -> None:

        if len(self.perm_jobs) >= self.bot.MAX_SELECT_OPTIONS:
            error = MaxItemsReached("Permanent Jobs", self.bot.MAX_SELECT_OPTIONS)
            await interaction.respond(embed=error, ephemeral=True)
            return

        prompt = U.make_embed(
            title="Permanent Jobs & Internships",
            description=(
                "We encourage venue owners and management to take advantage of the "
                "fresh-faced trainees that we have available. This option allows you "
                "to train staff members from the get go and ensure that they meet your "
                "venue's standards.\n\n"
                
                "**Would you like to take advantage of the Internship System?**"
            )
        )
        view = ConfirmCancelView(
            owner=interaction.user,
            confirm_text="Yes, I want to do an internship",
            cancel_text="No, I want experienced staff",
        )

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return

        if view.value is False:
            await self.jobs_manager.perm_job_wizard(interaction, self._parent)
        else:
            await self.jobs_manager.internship_wizard(interaction, self._parent)

################################################################################
    async def modify_perm_job(self, interaction: Interaction) -> None:

        job = await self._select_job(interaction, "Permanent", "Modify")
        if job is None:
            return

        await job.menu(interaction)

################################################################################
    async def remove_perm_job(self, interaction: Interaction) -> None:

        job = await self._select_job(interaction, "Permanent", "Remove")
        if job is None:
            return

        await job.remove(interaction)

################################################################################
