from __future__ import annotations

from datetime import datetime, timedelta, UTC
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Literal, Tuple
from zoneinfo import ZoneInfo

from discord import Interaction, ForumChannel, ButtonStyle, EmbedField, SelectOption, User, ChannelType, Member

from Enums import Month, Timezone, Position, MusicGenre
from UI.Common import ConfirmCancelView, FroggeSelectView, BasicTextModal, FroggeMultiMenuSelect, TimeSelectView, \
    InstructionsInfo
from Utilities import Utilities as U
from .PermanentJobPosting import PermanentJobPosting
from .TemporaryJobPosting import TemporaryJobPosting
from .TraineeMessage import TraineeMessage
from Classes.Common import RevisitTimer

if TYPE_CHECKING:
    from Classes import StaffPartyBot, Venue, Profile, Availability, VenueHours
################################################################################

__all__ = ("JobPostingManager", )

################################################################################
# noinspection PySimplifyBooleanCheck
class JobPostingManager:

    __slots__ = (
        "_state",
        "_temporary",
        "_permanent",
        "_trainee_msg",
        "_revisits",
    )

################################################################################
    def __init__(self, state: StaffPartyBot) -> None:

        self._state: StaffPartyBot = state

        self._temporary: List[TemporaryJobPosting] = []
        self._permanent: List[PermanentJobPosting] = []
        self._trainee_msg: TraineeMessage = TraineeMessage(state)
        self._revisits: List[RevisitTimer] = []

################################################################################
    async def load_all(self, payload: Dict[str, Any]) -> None:

        self._temporary = [TemporaryJobPosting(self, **p) for p in payload["temporary_jobs"]]
        self._permanent = [PermanentJobPosting(self, **p) for p in payload["permanent_jobs"]]

        for job in self.temporary_postings:
            await job.update_post_components(False)
        for job in self.permanent_postings:
            await job.update_post_components(False)

        self._trainee_msg.load(payload["trainee_message"])

        print("Loaded all job postings.")

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._state

################################################################################
    @property
    async def temp_jobs_channel(self) -> Optional[ForumChannel]:

        return await self.bot.channel_manager.temp_jobs_channel

################################################################################
    @property
    async def perm_jobs_channel(self) -> Optional[ForumChannel]:

        return await self.bot.channel_manager.perm_jobs_channel

################################################################################
    @property
    def temporary_postings(self) -> List[TemporaryJobPosting]:

        return self._temporary

################################################################################
    @property
    def permanent_postings(self) -> List[PermanentJobPosting]:

        return self._permanent

################################################################################
    async def temp_job_wizard(self, interaction: Interaction, v: Venue) -> None:

        prompt = U.make_embed(
            title="READ ME FIRST!",
            description=(
                "Please read the following instructions before proceeding.\n\n"
                
                "**You may select multiple positions at once to create\n"
                "temporary job postings for. These will utilize the default\n"
                "description and share the same start/end dates and salary.\n"
                "If you need to create a job posting with different details,\n"
                "you will need to create them one at a time.**"
            )
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        prompt = U.make_embed(
            title="Do You Need a DJ?",
            description="Are you posting a temporary job opening for a DJ?"
        )
        view = ConfirmCancelView(
            owner=interaction.user,
            confirm_text="Yes, I need a DJ",
            cancel_text="No, I need something else",
            cancel_style=ButtonStyle.primary
        )

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return

        if view.value is True:
            positions = [Position.DJ]
        else:
            prompt = U.make_embed(
                title="Temporary Job Posting",
                description=(
                    "Please select the jobs you want to create (a) temporary\n"
                    "job posting(s) for.\n\n"
                    
                    "You may select multiple positions at once, but they will\n"
                    "share the same details (salary, start/end dates, etc.)."
                )
            )
            base_options = Position.limited_select_options([Position.General_Training, Position.DJ])
            options = [o for o in base_options if o != Position.DJ]
            view = FroggeSelectView(interaction.user, options, multi_select=True)

            await interaction.respond(embed=prompt, view=view)
            await view.wait()

            if not view.complete or view.value is False:
                return

            positions = [Position(int(pos_id)) for pos_id in view.value]
            assert positions

        pos_descriptions = { p: p.description for p in positions }
        prompt = U.make_embed(
            title="Job Description(s)",
            description=(
                "Would you like to use the default description for this/these\n"
                "job posting(s), or would you like to provide a custom one?\n\n"
                
                "The following are the default descriptions for each position "
                "you selected."
            ),
            fields=[
                EmbedField(
                    name=p.proper_name,
                    value=p.description or "`No description provided.`",
                    inline=True
                ) for p in positions
            ]
        )
        view = ConfirmCancelView(
            owner=interaction.user,
            confirm_text="Use Custom",
            cancel_text="Use Default",
            confirm_style=ButtonStyle.primary,
            cancel_style=ButtonStyle.primary,
        )

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return

        inter = interaction

        if view.value is True:
            prompt = U.make_embed(
                title="Job Description(s)",
                description=(
                    "Please select the jobs you want to enter a custom description for.\n\n"
                    
                    "The following are the default descriptions for each position you selected."
                ),
                fields=[
                    EmbedField(
                        name=p.proper_name,
                        value=p.description or "`No description provided.`",
                        inline=True
                    ) for p in positions
                ]
            )
            view = FroggeSelectView(
                owner=interaction.user,
                options=[p.select_option for p in positions],
                multi_select=True,
                return_interaction=True,
                close_text="Skip"
            )

            await interaction.respond(embed=prompt, view=view)
            await view.wait()

            if not view.complete:
                return

            if view.value is not False:
                pos_ids, inter = view.value
                positions_to_update = [Position(int(i)) for i in pos_ids]

                count = 1
                for pos in positions_to_update:
                    modal = BasicTextModal(
                        title="Temporary Job Posting",
                        attribute="Job Description",
                        max_length=250,
                        required=False,
                        return_interaction=True,
                        instructions=InstructionsInfo(
                            placeholder="Change your job's description text below.",
                            value=(
                                f"Please provide a custom description for your "
                                f"**{pos.proper_name}** job posting."
                            )
                        )
                    )

                    await inter.response.send_modal(modal)
                    await modal.wait()

                    if not modal.complete:
                        return

                    if modal.value:
                        description, inter = modal.value
                        pos_descriptions[pos] = description

                    if len(positions_to_update) > 1 and count < len(positions_to_update):
                        prompt = U.make_embed(
                            title="Job Description(s)",
                            description=(
                                "**Would you like to enter a custom description "
                                "for one of the other positions?**"
                            )
                        )
                        view = ConfirmCancelView(
                            owner=inter.user,
                            return_interaction=True,
                            confirm_text="Yes",
                            cancel_text="Done",
                            cancel_style=ButtonStyle.primary
                        )

                        await inter.respond(embed=prompt, view=view)
                        await view.wait()

                        if not view.complete:
                            return

                        if view.value is False:
                            break

                        _, inter = view.value
                        count += 1

        prompt = U.make_embed(
            title="Job Salary",
            description=(
                "Next you will need to enter the salary for this/these "
                "job posting(s).\n\n"

                "**Leave the field blank if you want to skip this step.**"
            )
        )
        view = ConfirmCancelView(
            owner=interaction.user,
            return_interaction=True,
            show_cancel=False
        )

        await inter.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        _, inter = view.value

        modal = BasicTextModal(
            title="Job Posting Salary",
            attribute="Salary",
            max_length=50,
            return_interaction=True
        )

        await inter.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        salary, inter = modal.value

        start_result = await self._collect_datetime(inter, "Start")
        if start_result is None:
            return
        start_dt, tz = start_result

        if start_dt < datetime.now(UTC):
            error = U.make_embed(
                title="Invalid Start Time",
                description=(
                    "The start time for a job posting must be in the future.\n"
                    "Please try again."
                )
            )
            await inter.respond(embed=error, ephemeral=True)
            return

        options = []
        for total_minutes in range(30, 361, 30):
            hours = total_minutes // 60
            leftover = total_minutes % 60

            # Build a human-friendly label: e.g., "1h 30m", "30m", "6h"
            if hours > 0 and leftover > 0:
                label = f"{hours}h {leftover}m"
            elif hours > 0:
                label = f"{hours}h"
            else:
                label = f"{leftover}m"

            options.append(SelectOption(label=label, value=str(total_minutes)))

        prompt = U.make_embed(
            title="Job Posting Length",
            description="How long will this job posting last?"
        )
        view = FroggeSelectView(interaction.user, options)

        await inter.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        end_dt = start_dt + timedelta(minutes=int(view.value))

        genres = None
        if Position.DJ in positions:
            prompt = U.make_embed(
                title="DJ Genre",
                description=(
                    "Please select the genre of music you would like your DJ to play."
                )
            )
            view = FroggeSelectView(interaction.user, MusicGenre.select_options(), multi_select=True)

            await interaction.respond(embed=prompt, view=view)
            await view.wait()

            if not view.complete or view.value is False:
                return

            genres = [MusicGenre(int(g)) for g in view.value]

        for pos, descr in pos_descriptions.items():
            new_job = TemporaryJobPosting.new(
                self, v, interaction.user, pos, descr, salary,
                start_dt, end_dt, genres, tz
            )
            self._temporary.append(new_job)

            await new_job.create_post(inter)
            await inter.respond(
                "Job posting created!\n\n"

                f"**Venue:** {v.name}\n"
                f"**Position:** {pos.proper_name}\n"
                f"**Description:** {descr}\n"
                f"**Salary:** {salary}\n"
                f"**Start:** {U.format_dt(start_dt)}\n"
                f"**End:** {U.format_dt(end_dt)}\n"
                f"[View Job Posting]({new_job.post_url})",
                ephemeral=True
            )

################################################################################
    @staticmethod
    async def _collect_datetime(
        interaction: Interaction,
        date_type: Literal["Start", "End"],
        tz: Optional[ZoneInfo] = None
    ) -> Optional[Tuple[datetime, ZoneInfo]]:

        if tz is None:
            prompt = U.make_embed(
                title=f"Job Posting Timezone",
                description=f"Please select the timezone for this job posting."
            )
            view = FroggeSelectView(interaction.user, Timezone.select_options())

            await interaction.respond(embed=prompt, view=view)
            await view.wait()

            if not view.complete or view.value is False:
                return None

            tz = U.TIMEZONE_OFFSETS[Timezone(int(view.value))]

        prompt = U.make_embed(
            title=f"Job Posting {date_type} Time",
            description=f"Please select the month this job posting {date_type.lower()}s in."
        )
        view = FroggeSelectView(interaction.user, Month.select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return None

        month = Month(int(view.value))

        prompt = U.make_embed(
            title=f"Job Posting {date_type} Time",
            description=f"Please select the day this job posting {date_type.lower()}s on."
        )
        options = [SelectOption(label=str(i), value=str(i)) for i in range(1, month.days() + 1)]
        view = FroggeMultiMenuSelect(interaction.user, options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return None

        day = int(view.value)

        prompt = U.make_embed(
            title=f"Job Posting {date_type} Time",
            description=(
                f"Please select the year of this job posting's "
                f"{date_type.lower()} time."
            )
        )
        cur_year = datetime.now().year
        options = [SelectOption(label=str(i), value=str(i)) for i in range(cur_year, cur_year + 2)]
        view = FroggeSelectView(interaction.user, options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return None

        year = int(view.value)

        prompt = U.make_embed(
            title=f"Job Posting {date_type} Time",
            description=(
                f"Please select the hour, then minute increment of this job posting's "
                f"{date_type.lower()} time."
            )
        )
        view = TimeSelectView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return None

        hours, minutes = view.value
        return datetime(
            year=year,
            month=month.value,
            day=day,
            hour=hours,
            minute=minutes,
            tzinfo=tz
        ), tz

################################################################################
    async def cull_postings(self) -> None:

        temporary_jobs_channel = await self.temp_jobs_channel
        if temporary_jobs_channel is None:
            return

        for posting in self._temporary:
            await posting.expiration_check()

        assert isinstance(temporary_jobs_channel, ForumChannel)
        for thread in temporary_jobs_channel.threads:
            count = 0
            async for _ in thread.history():
                count += 1
            if count == 0:
                await thread.delete()

################################################################################
    async def perm_job_wizard(self, interaction: Interaction, v: Venue) -> None:

        prompt = U.make_embed(
            title="Permanent Job Posting",
            description=(
                "Please select the jobs you want to create (a) permanent\n"
                "job posting(s) for.\n\n"

                "You may select multiple positions at once, but they will\n"
                "share the same salary information."
            )
        )
        view = FroggeSelectView(
            owner=interaction.user,
            options=Position.limited_select_options([Position.General_Training, Position.DJ]),
            multi_select=True
        )

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        positions = [Position(int(pos_id)) for pos_id in view.value]
        assert positions
        pos_descriptions = { p: p.description for p in positions }

        prompt = U.make_embed(
            title="Job Description(s)",
            description=(
                "Would you like to use the default description for this/these\n"
                "job posting(s), or would you like to provide a custom one?\n\n"

                "The following are the default descriptions for each position you selected."
            ),
            fields=[
                EmbedField(
                    name=p.proper_name,
                    value=p.description or "`No description provided.`",
                    inline=True
                ) for p in positions
            ]
        )
        view = ConfirmCancelView(
            owner=interaction.user,
            confirm_text="Use Custom",
            cancel_text="Use Default",
            confirm_style=ButtonStyle.primary,
            cancel_style=ButtonStyle.primary,
        )

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return

        inter = interaction

        if view.value is True:
            prompt = U.make_embed(
                title="Job Description(s)",
                description=(
                    "**Please select the job you want to enter a "
                    "custom description for.**\n\n"

                    "The following are the default descriptions for each position you selected."
                ),
                fields=[
                    EmbedField(
                        name=p.proper_name,
                        value=pos_descriptions[p] or "`No description provided.`",
                        inline=True
                    ) for p in positions
                ]
            )
            view = FroggeSelectView(
                owner=interaction.user,
                options=[p.select_option for p in positions],
                multi_select=True,
                return_interaction=True,
                close_text = "Skip"
            )

            await inter.respond(embed=prompt, view=view)
            await view.wait()

            if not view.complete:
                return

            if view.value is not False:
                pos_ids, inter = view.value
                positions_to_update = [Position(int(i)) for i in pos_ids]

                count = 1
                for pos in positions_to_update:
                    modal = BasicTextModal(
                        title="Permanent Job Posting",
                        attribute="Job Description",
                        required=False,
                        max_length=500,
                        return_interaction=True,
                        instructions=InstructionsInfo(
                            placeholder="Change your job's description text below.",
                            value=(
                                f"Please provide a custom description for your "
                                f"**{pos.proper_name}** job posting."
                            )
                        )
                    )

                    await inter.response.send_modal(modal)
                    await modal.wait()

                    if not modal.complete:
                        return

                    if modal.value:
                        description, inter = modal.value
                        pos_descriptions[pos] = description

                    if len(positions_to_update) > 1 and count < len(positions_to_update):
                        prompt = U.make_embed(
                            title="Job Description(s)",
                            description=(
                                "**Would you like to enter a custom description "
                                "for one of the other positions?**"
                            )
                        )
                        view = ConfirmCancelView(
                            owner=inter.user,
                            return_interaction=True,
                            confirm_text="Yes",
                            cancel_text="Done",
                            cancel_style=ButtonStyle.primary
                        )

                        await inter.respond(embed=prompt, view=view)
                        await view.wait()

                        if not view.complete:
                            return

                        if view.value is False:
                            break

                        _, inter = view.value
                        count += 1

        prompt = U.make_embed(
            title="Job Salary",
            description=(
                "Next you may enter the salary for this/these job posting(s).\n\n"
                
                "**Leave the field blank if you want to skip this step.**"
            )
        )
        view = ConfirmCancelView(interaction.user, return_interaction=True, show_cancel=False)

        await inter.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        _, inter = view.value

        modal = BasicTextModal(
            title="Job Posting Salary",
            attribute="Salary",
            max_length=200,
            required=False,
        )

        await inter.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        salary = modal.value or None

        for pos, descr in pos_descriptions.items():
            new_job = PermanentJobPosting.new(self, v, interaction.user, pos, descr, salary)
            self._permanent.append(new_job)

            await new_job.create_post(inter)
            await inter.respond(
                "Job posting created!\n\n"

                f"**Venue:** {v.name}\n"
                f"**Position:** {pos.proper_name}\n"
                f"**Description:** {descr}\n"
                f"**Salary:** {salary or '`Not Provided`'}\n"
                f"[View Job Posting]({new_job.post_url})",
                ephemeral=True,
            )

################################################################################
    def _get_trainee_matches(self, venue: Venue, position: Position) -> Dict[Profile, int]:
        """
        Returns a list of Profiles who want training for the given position,
        are on the same data center, and have availability covering the venue's schedule.
        Then also calculates a "compatibility percentage" based on comparing
        the venue's RP level / tags to each profile's.
        """

        def matches_hours(avail: Availability, hours: VenueHours) -> bool:
            """
            Returns True if at least one hour of availability overlaps with the venue's open hours.
            Supports crossing midnight (e.g., 15:00–03:00).
            """

            def to_minutes_with_wrap(start, end):
                s = start.hour * 60 + start.minute
                e = end.hour * 60 + end.minute
                if e <= s:
                    e += 1440  # Treat end as next day if it wraps past midnight
                return s, e

            avail_s, avail_e = to_minutes_with_wrap(avail.start_time, avail.end_time)
            hrs_s, hrs_e = to_minutes_with_wrap(hours.start_time, hours.end_time)

            # Find overlap in minutes
            overlap_start = max(avail_s, hrs_s)
            overlap_end = min(avail_e, hrs_e)
            overlap_duration = overlap_end - overlap_start

            return overlap_duration >= 60

        # First, gather all profiles who want training (bot-side logic).
        ret = self.bot.profile_manager.profiles_wanting_training()

        # Filter out profiles that don't match position, data center, or schedule
        # Note: removing from a list while iterating can be brittle.
        #       A safer approach is to build a new list with the matches.
        filtered = []
        for profile in ret:
            # 1) Must desire 'position'
            if position not in profile.desired_trainings:
                continue
            # 2) Must share a data center with the venue
            if not any(dc.contains(venue.location.data_center) for dc in profile.data_centers):
                continue
            # 3) Must have availability covering at least one of the venue's scheduled hours
            if not any(matches_hours(avail, hours) for avail in profile.availability for hours in venue.schedule):
                continue
            # 4) NSFW preference must match venue's NSFW status
            if venue.nsfw:
                if not profile.nsfw_preference:
                    continue

            filtered.append(profile)
            if len(filtered) >= 9: # Limit to 9 profiles for looks
                break

        # Make 'filtered' the final list
        ret = filtered

        # Start everyone at 100% compatibility
        pct_dict = {profile: 100 for profile in ret}

        # Compare RP Level & Tags to reduce or adjust the percentage
        for profile in ret:
            # 1) Compare RP Level
            #    Let's assume your RP enum can be cast to an integer or has a .value attribute.
            #    The bigger the difference in levels, the more we reduce compatibility.
            #    For example: 0 difference => no penalty, difference of 4 => big penalty.
            venue_rp_value = venue.rp_level.value  # e.g. integer from 0..4
            profile_rp_value = profile.rp_level.value
            rp_diff = abs(venue_rp_value - profile_rp_value)

            # Simple penalty example: 10% penalty per difference in RP level
            rp_penalty = 10 * rp_diff

            # 2) Compare Tags
            #    Suppose we do a simple overlap-based bonus or penalty.
            #    Example: If the venue has "tags = ['Nightlife','18+','LGBTQ+']"
            #    and the profile has "['Nightlife','Roleplay','All Ages']",
            #    then the overlap is 1 out of the venue's 3 tags.
            venue_tags = set(venue.tags)
            profile_tags = set(profile.venue_tags)
            overlap = venue_tags.intersection(profile_tags)

            # Let's say for every missing venue tag, we take a penalty,
            # or for every matched tag, we do no penalty.
            # You can do something more complex or a small bonus for each match.
            # Here, let's do a negative penalty for each mismatch:
            total_venue_tags = len(venue_tags)
            matched_tags = len(overlap)
            missing_count = total_venue_tags - matched_tags

            # For each missing tag, reduce 5% or so
            tag_penalty = 5 * missing_count

            # Combine the penalties.
            # Alternatively, you could store them separately or do a more weighted approach.
            total_penalty = rp_penalty + tag_penalty

            # Apply the penalty to the existing 100% base (clamp at 0 if it goes negative).
            new_pct = max(0, pct_dict[profile] - total_penalty)
            pct_dict[profile] = new_pct

        # Debug / check results:
        for p, pct in pct_dict.items():
            print(p.char_name, pct)

        return pct_dict

################################################################################
    async def internship_wizard(self, interaction: Interaction, parent: Venue) -> None:

        prompt = U.make_embed(
            title="Select Internship Job Type",
            description=(
                "Please select the type of internship you would like to create."
            )
        )
        view = FroggeSelectView(interaction.user, Position.limited_select_options([Position.DJ]))

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        position = Position(int(view.value))
        matches = self._get_trainee_matches(parent, position)

        if not matches:
            problem = U.make_embed(
                title="No Matches Found",
                description=(
                    "No prospective employee matches were found that fit your "
                    "internship criteria."
                )
            )
            await interaction.respond(embed=problem, ephemeral=True)
            return

        prompt = U.make_embed(
            title="Trainee Matches",
            description=(
                "The following potential staff are available for training at your venue.\n\n"
                
                "Please select the profiles you would like to message.\n\n"
                
                "**NOTE: This will open a new thread with the selected users.**"
            ),
            fields=[
                EmbedField(
                    name=profile.char_name,
                    value=(
                        f"Match: {pct}%\n"
                        f"[(View Profile)]({profile.post_url})\n"
                    ),
                    inline=True
                ) for profile, pct in matches.items()
            ]
        )
        options = [
            SelectOption(
                label=profile.char_name,
                value=str(profile.id),
                description=f"Compatibility: {pct}%",
            )
            for profile, pct in matches.items()
        ]
        view = FroggeSelectView(interaction.user, options, multi_select=True)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        user_ids = [int(p_id) for p_id in view.value]
        for user_id in user_ids:
            user = await self.bot.get_or_fetch_user(user_id)
            await self.initiate_communication(interaction, user, parent)

################################################################################
    async def initiate_communication(self, interaction: Interaction, user: User, v: Venue) -> None:

        parent_channel = await self.bot.channel_manager.internship_channel
        if parent_channel is None:
            error = U.make_error(
                title="Channel Missing",
                message="The parent thread channel for internships is missing.",
                solution="Please contact a bot administrator."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        post_message = (
            f"Hello {user.mention},\n\n"
            
            f"{interaction.user.mention} from [{v.name}]({v.post_url}) is interested in "
            f"offering {user.mention} a training position at their venue.\n\n"
            
            "Please utilize this thread to further discuss the details of "
            "your internship!"
        )
        thread = await parent_channel.create_thread(
            name=f"Internship with {user.display_name}",
            type=ChannelType.private_thread,
            auto_archive_duration=4320  # 3 days
        )
        await thread.send(post_message)

        await thread.add_user(interaction.user)
        await thread.add_user(user)

        notify = U.make_embed(
            title="Internship Initiated",
            description=(
                f"{interaction.user.display_name} from [{v.name}]({v.post_url}) has "
                f"initiated an internship thread with {user.mention}.\n\n"
                
                "[Please head over here to discuss the details of your partnership!]"
                f"({thread.jump_url})"
            )
        )

        try:
            await user.send(embed=notify)
        except Exception:
            pass

        try:
            await interaction.user.send(embed=notify)
        except Exception:
            pass

################################################################################
    async def on_member_leave(self, member: Member) -> Tuple[int, int]:

        removed = 0
        reopened = 0

        for temp_job in self._temporary:
            if temp_job._user.id == member.id:
                await temp_job.poster_left()
                removed += 1
            elif temp_job._candidate.id == member.id:
                await temp_job.cancel(None)
                reopened += 1

        for perm_job in self._permanent:
            if perm_job._user.id == member.id:
                await perm_job.delete()
                removed += 1

        return removed, reopened

################################################################################
    async def check_revisits(self):

        final = []

        for revisit in self._revisits:
            if revisit.is_expired():
                await revisit.context.revisit()
            else:
                final.append(revisit)

        self._revisits = final

################################################################################
    def register_revisit(self, posting: PermanentJobPosting, duration_sec: int = 30) -> None:  # 3 days

        self._revisits.append(RevisitTimer(posting, duration_sec))

################################################################################
