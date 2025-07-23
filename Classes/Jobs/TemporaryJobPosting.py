from __future__ import annotations

from datetime import datetime, UTC, timedelta
from zoneinfo import ZoneInfo
from typing import TYPE_CHECKING, Optional, Type, TypeVar, List, Any, Dict

from discord import (
    User,
    Embed,
    Message,
    Interaction,
    ForumChannel,
    EmbedField,
    HTTPException, SelectOption, ChannelType, Thread
)

from Assets import BotEmojis
from Classes.Common import Identifiable, LazyUser, LazyMessage
from Enums import Weekday, Position, MusicGenre, Timezone, Month, TimeType, Hours, Minutes
from UI.Jobs import JobPostingPickupView, TemporaryJobPostingStatusView, JobTimeButtonsView, JobTimeComponentView
from Utilities import Utilities as U
from UI.Common import ConfirmCancelView, BasicTextModal, FroggeSelectView, FroggeMultiMenuSelect, TimeSelectView

if TYPE_CHECKING:
    from Classes import JobPostingManager, Venue, StaffPartyBot
################################################################################

__all__ = ("TemporaryJobPosting",)

JP = TypeVar("JP", bound="TemporaryJobPosting")

################################################################################
class TemporaryJobPosting(Identifiable):

    __slots__ = (
        "_mgr",
        "_user",
        "_venue_id",
        "_position",
        "_salary",
        "_start",
        "_end",
        "_description",
        "_post_msg",
        "_candidate",
        "_schedule_updated",
        "_genres",
        "_tz",
    )

################################################################################
    def __init__(self, mgr: JobPostingManager, id: int, **kwargs) -> None:

        super().__init__(id)

        self._mgr: JobPostingManager = mgr
        self._user = LazyUser(mgr, kwargs.pop("user_id"))

        self._venue_id: int = kwargs.pop("venue_id")
        self._candidate: LazyUser = LazyUser(self, kwargs.get("candidate_id"))

        self._description: str = kwargs.pop("description")
        self._position: Position = Position(kwargs.pop("position_id"))
        self._genres: List[MusicGenre] = [
            MusicGenre(g)
            for g
            in kwargs.get("genres", [])
        ]
        self._post_msg: LazyMessage = LazyMessage(self, kwargs.get("post_url"))

        self._salary: str = kwargs.get("salary")
        self._start: datetime = kwargs.get("start_dt").replace(tzinfo=ZoneInfo("UTC"))
        self._end: datetime = kwargs.get("end_dt").replace(tzinfo=ZoneInfo("UTC"))

        self._schedule_updated: bool = False
        self._tz: Optional[ZoneInfo] = kwargs.get("timezone", None)

################################################################################
    @classmethod
    def new(
        cls: Type[JP],
        mgr: JobPostingManager,
        venue: Venue,
        user: User,
        position: Position,
        description: str,
        salary: str,
        start_dt: datetime,
        end_dt: datetime,
        genres: Optional[List[MusicGenre]] = None,
        tz: Optional[ZoneInfo] = None
    ) -> JP:

        new_data = mgr.bot.db.insert.temporary_job(
            venue_id=venue.id,
            user_id=user.id,
            position_id=position.value,
            description=description,
            salary=salary,
            start_dt=start_dt,
            end_dt=end_dt,
            genres=[g.value for g in genres] if genres else []
        )
        new_data["timezone"] = tz
        return cls(mgr, **new_data)

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._mgr.bot

################################################################################
    @property
    async def posting_user(self) -> User:

        return await self._user.get()

################################################################################
    @property
    async def post_channel(self) -> Optional[ForumChannel]:

        return await self._mgr.temp_jobs_channel

################################################################################
    @property
    async def post_message(self) -> Optional[Message]:

        return await self._post_msg.get()

    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:

        self._post_msg.set(value)

    @property
    def post_url(self) -> Optional[str]:

        return self._post_msg.id

################################################################################
    @property
    async def candidate(self) -> Optional[User]:

        return await self._candidate.get()

    @candidate.setter
    def candidate(self, value: Optional[User]) -> None:

        self._candidate.set(value)

    @property
    def is_accepted(self) -> bool:

        return self._candidate.id is not None

################################################################################
    @property
    def description(self) -> Optional[str]:

        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:

        self._description = value
        self.update()

################################################################################
    @property
    def salary(self) -> Optional[str]:

        return self._salary

    @salary.setter
    def salary(self, value: Optional[str]) -> None:

        self._salary = value
        self.update()

################################################################################
    @property
    def timezone(self) -> Optional[ZoneInfo]:

        return self._tz

    @property
    def start_time(self) -> datetime:

        return self._start

################################################################################
    def _set_schedule_impl(self, start: datetime, end: datetime) -> None:

        self._start = start.astimezone(UTC)
        self._end = end.astimezone(UTC)
        self._schedule_updated = True
        self.update()

################################################################################
    @property
    def position(self) -> Position:

        return self._position

################################################################################
    @property
    def genres(self) -> List[MusicGenre]:

        return self._genres

################################################################################
    @property
    def venue(self) -> Venue:

        return self.bot.venue_manager[self._venue_id]

################################################################################
    @property
    def is_dj_posting(self) -> bool:

        return self.position == Position.DJ

################################################################################
    def update(self) -> None:

        self.bot.db.update.temporary_job(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "description": self._description,
            "salary": self._salary,
            "start_dt": self._start,
            "end_dt": self._end,
            "post_url": self._post_msg.url,
            "candidate_id": self._candidate.id if self._candidate else None,
            "genres": [g.value for g in self._genres],
        }

################################################################################
    async def delete(self) -> None:

        self.bot.db.delete.temporary_job(self.id)

        post_message = await self.post_message
        if post_message:
            try:
                await post_message.delete()
            except Exception:
                pass

        self._mgr._temporary.remove(self)

################################################################################
    async def status(self) -> Embed:

        hours = (self._end - self._start).total_seconds() / 3600
        time_field_value = f"`{hours:.2f} hours`"

        posting_user = await self.posting_user
        return U.make_embed(
            title=f"Job Posting Status",
            description=(
                "__**Venue Name:**__\n"
                f"`{self.venue.name}`\n\n"
    
                "__**Venue Contact:**__\n"
                f"`{posting_user.display_name}`\n"
                f"({posting_user.mention})\n\n"
    
                "__**Venue Address:**\n"
                f"`{self.venue.location.format()}`\n\n"
    
                "__**Job Description:**__\n"
                f"{U.wrap_text(self._description or '`No Description`', 50)}\n\n"
    
                f"{U.draw_line(extra=30)}\n"
            ),
            fields=[
                EmbedField(
                    name="__Position__",
                    value=f"`{self._position.proper_name}`",
                    inline=True
                ),
                EmbedField(
                    name="__Salary__",
                    value=self._salary,
                    inline=False
                ),
                EmbedField(
                    name="__Start Time__",
                    value=(
                        f"{U.format_dt(self._start, 'F')}\n\n"

                        f"__**End Time**__\n"
                        f"{U.format_dt(self._end, 'F')}\n"
                        f"{U.draw_line(extra=12)}"
                    ),
                    inline=True
                ),
                EmbedField(
                    name="__Total Time__",
                    value=time_field_value,
                    inline=True
                ),
                EmbedField(
                    name="__Posting URL__",
                    value=(
                        f"{BotEmojis.ArrowRight}{BotEmojis.ArrowRight}{BotEmojis.ArrowRight} "
                        f"[Click here to view the posting]({self.post_url}) "
                        f"{BotEmojis.ArrowLeft}{BotEmojis.ArrowLeft}{BotEmojis.ArrowLeft}"
                    ) if self.post_url is not None else "`Not Posted`",
                    inline=False
                ),
            ],
        )

################################################################################
    async def menu(self, interaction: Interaction) -> None:

        embed = await self.status()
        view = TemporaryJobPostingStatusView(interaction.user, self)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    async def compile(self) -> Embed:

        managers = await self.venue.managers
        manager_str = "\n".join([f"- {m.mention} ({m.display_name})" for m in managers])

        description = (
            "__**Venue Contacts:**__\n"
            f"{manager_str}\n\n"

            "__**Venue Address:**__\n"
            f"`{self.venue.location.format()}`\n\n"

            "__**Job Description:**__\n"
            f"{U.wrap_text(self._description, 50)}\n"

            f"{U.draw_line(extra=30)}\n"
        )
        fields = [
            EmbedField(
                name="__Position__",
                value=f"`{self.position.proper_name}`",
                inline=True
            ),
            EmbedField(
                name="__Salary__",
                value=self._salary,
                inline=False
            )
        ]
        if self.position == Position.DJ:
            assert self.genres
            fields.append(
                EmbedField(
                    name="__Desired Genres__",
                    value=", ".join([f"`{g.proper_name}`" for g in self.genres]),
                    inline=False
                )
            )

        fields.append(
            EmbedField(
                name="__Start Time__",
                value=(
                    f"{U.format_dt(self._start, 'F')}\n\n"

                    f"__**End Time**__\n"
                    f"{U.format_dt(self._end, 'F')}\n"
                    f"{U.draw_line(extra=12)}"
                ),
                inline=True
            )
        )

        return U.make_embed(
            title=f"`{self.position.proper_name}` Needed at `{self.venue.name}`",
            description=description,
            fields=fields,
            thumbnail_url=self.venue.urls.logo
        )

################################################################################
    async def create_post(self, interaction: Interaction) -> None:

        channel = await self.post_channel
        if channel is None:
            error = U.make_error(
                title="No Job Posting Channel",
                message="There is no channel set up for job postings.",
                solution="Please contact a server administrator."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return
        assert isinstance(channel, ForumChannel)

        if await self.update_post_components(True, True):
            confirm = U.make_embed(
                title="Job Posting Updated",
                description="The job posting has been updated."
            )
            await interaction.respond(embed=confirm, ephemeral=True)

            if self._schedule_updated:
                await self.notify_eligible_applicants()
                self._schedule_updated = False
            return

        post_view = JobPostingPickupView(self)
        self.bot.add_view(post_view)

        pos_thread = next((t for t in channel.threads if t.name.lower() == self.position.proper_name.lower()), None)
        try:
            if pos_thread is not None:
                self.post_message = await pos_thread.send(embed=await self.compile(), view=post_view)
            else:
                pos_thread = await channel.create_thread(name=self.position.proper_name, embed=await self.compile(), view=post_view)
                self.post_message = pos_thread.last_message

        except Exception as ex:
            error = U.make_embed(
                title="Posting Error",
                description=f"There was an error posting the job listing.\n\n{ex}"
            )
            await interaction.respond(embed=error, ephemeral=True)
        else:
            await self.bot.log.temp_job_posted(self)
            await self.notify_eligible_applicants()

################################################################################
    async def update_post_components(
        self,
        update_status: bool,
        update_view: bool = True,
        _addl_attempt: bool = False
    ) -> bool:

        post_message = await self.post_message
        if post_message is None:
            self.post_message = None
            return False

        if update_status and not update_view:
            await post_message.edit(embed=await self.compile())
            return True

        view = JobPostingPickupView(self)
        self.bot.add_view(view, message_id=self._post_msg.id)

        try:
            if update_view and not update_status:
                await post_message.edit(view=view)
            else:
                await post_message.edit(embed=await self.compile(), view=view)
        except HTTPException as ex:
            if ex.code != 50083 and not _addl_attempt:
                return False
            await post_message.channel.send("Hey Ur Cute", delete_after=0.1)
            await self.update_post_components(True, _addl_attempt=True)
            return True
        else:
            return True

################################################################################
    async def is_user_eligible(
        self,
        user: User,
        compare_data_centers: bool,
        compare_schedule: bool,
        check_profile: bool,
        check_nsfw: bool = True,
        check_tags: bool = False,
        check_mutes: bool = True
    ) -> bool:

        # Check user and venue mute lists
        if user in await self.venue.muted_users:
            return False

        profile = self.bot.profile_manager.get_profile(user.id)
        if check_mutes:
            if self.venue in profile.muted_venues:
                return False

        if check_profile:
            profile_post_message = await profile.post_message
            if profile_post_message is None:
                return False

        if check_nsfw:
            if self.venue.nsfw and not profile.nsfw_preference:
                return False

        if check_tags:
            tag_strs = [t.proper_name for t in profile._main_info.preferred_tags]
            venue_tags = self.venue.tags
            if not any(tag in venue_tags for tag in tag_strs):
                return False

        # Check if job's data center is in the user's data centers list
        if compare_data_centers and len(profile.data_centers) > 0:
            if not any(dc.contains(self.venue.location.data_center) for dc in profile.data_centers):
                return False

        # If comparing schedules, check if the user is available during the job's times
        if compare_schedule and check_profile:
            job_day = Weekday(self._start.weekday())
            for availability in profile.details.availability:
                if availability.day == job_day:
                    start_time, end_time = self._start.time(), self._end.time()
                    if availability.contains(start_time, end_time):
                        return True
            return False  # If no matching availability was found

        # If not comparing schedules or none of the above conditions matched, the user is eligible
        return True

################################################################################
    async def is_dj_eligible(
        self,
        user: User,
        compare_data_centers: bool,
        compare_schedule: bool,
        check_profile: bool,
        check_nsfw: bool = True,
        check_genres: Optional[List[MusicGenre]] = None,
    ) -> bool:

        # Check user and venue mute lists
        if user in await self.venue.muted_users:
            return False

        profile = self.bot.dj_profile_manager.get_profile(user.id)
        # if self.venue in profile.muted_venues:
        if self.venue in []:
            return False

        if check_profile:
            profile_post_message = await profile.post_message
            if profile_post_message is None:
                return False

        if check_nsfw:
            if self.venue.nsfw and not profile.nsfw:
                return False

        if check_genres is not None:
            assert len(check_genres) > 0
            if not any(genre in profile.genres for genre in check_genres):
                return False

        # Check if job's data center is in the user's data centers list
        if compare_data_centers:
            if not any(r.contains(self.venue.location.data_center) for r in profile.regions):
                return False

        # If comparing schedules, check if the user is available during the job's times
        if compare_schedule and check_profile:
            job_day = Weekday(self._start.weekday())
            for availability in profile.availability:
                if availability.day == job_day:
                    start_time, end_time = self._start.time(), self._end.time()
                    print(start_time, end_time)
                    if availability.contains(start_time, end_time):
                        return True
            return False  # If no matching availability was found

        # If not comparing schedules or none of the above conditions matched, the user is eligible
        return True

################################################################################
    async def candidate_accept(self, interaction: Interaction) -> None:

        if not await self.is_user_eligible(
            interaction.user,
            compare_data_centers=False,
            compare_schedule=False,
            check_profile=True,
            check_nsfw=False,
            check_tags=False,
            check_mutes=False
        ):
            error = U.make_error(
                title="Ineligible for Job",
                message="You are not eligible for this job.",
                solution=(
                    "Please ensure you have selected the appropriate "
                    "pingable role in the server and that your staff profile"
                    "has been completed and posted!\n"
                )
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        profile = self.bot.profile_manager.get_profile(interaction.user.id)
        if self.venue in profile.muted_venues:
            error = U.make_error(
                title="Muted Venue",
                message=(
                    "You have muted in this venue in the past, and therefore "
                    "cannot accept this job posting."
                ),
                solution=(
                    "Please contact an SPB administrator if you believe this "
                    "is an error."
                )
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        self.candidate = interaction.user
        await self.update_post_components(True)
        await interaction.edit()

        thread = await self._open_thread(interaction)
        jump_url = thread.jump_url if thread else None
        if jump_url:
            final_sentence = (
                f"[Click here]({jump_url}) to view the thread."
            )
        else:
            final_sentence = (
                "Unable to create a thread for this job posting."
            )

        notify = U.make_embed(
            title="Job Accepted",
            description=(
                f"__**Position**__\n"
                f"`{self.position.proper_name}`\n"
                f"*({self.venue.name})*\n\n"

                f"__**Picked Up By**__\n"
                f"`{interaction.user.display_name}`\n"
                f"{final_sentence}"
            )
        )

        try:
            to_notify = await self.posting_user
            await to_notify.send(embed=notify)
        except Exception:
            pass

        await self.bot.log.job_accepted(self)

################################################################################
    async def _open_thread(self, interaction: Interaction) -> Optional[Thread]:

        parent_channel = await self.bot.channel_manager.communication_channel
        if parent_channel is None:
            error = U.make_error(
                title="Channel Missing",
                message="The parent thread channel for internships is missing.",
                solution="Please contact a bot administrator."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return None

        poster = await self.posting_user
        post_message = (
            f"Hello {interaction.user.mention},\n\n"

            f"{poster.mention} is interested in hiring you for the "
            f"`{self.position.proper_name}` temporary position at their venue.\n\n"

            "Please utilize this thread to further discuss the details of "
            "your hiring!"
        )
        thread = await parent_channel.create_thread(
            name=f"Temp Job with {interaction.user.display_name}",
            type=ChannelType.private_thread,
            auto_archive_duration=4320  # 3 days
        )
        await thread.send(post_message)

        return thread

################################################################################
    async def cancel(self, interaction: Optional[Interaction] = None) -> None:

        candidate = await self.candidate
        if candidate is None:
            return

        # Log before removing the candidate
        await self.bot.log.job_canceled(self)

        self.candidate = None
        await self.update_post_components(True)

        if interaction is not None:
            await interaction.edit()

        notify = U.make_embed(
            title="Job Canceled",
            description=(
                f"__**Position**__\n\n"
                f"`{self.position.proper_name}`\n"
                f"*({self.venue.name})*\n\n"

                "The previous candidate has removed themself from this job posting.\n\n"

                "For your convenience, the posting has been re-activated and "
                "is now available for other applicants to accept."
            )
        )

        try:
            to_notify = await self.posting_user
            await to_notify.send(embed=notify)
        except Exception:
            pass

################################################################################
    async def expiration_check(self) -> None:

        if self._end.timestamp() <= datetime.now().timestamp():
            await self.delete()

################################################################################
    async def notify_eligible_applicants(self) -> None:

        if self.is_dj_posting:
            eligible = [
                profile for profile in self.bot.dj_profile_manager.profiles
                if await self.is_dj_eligible(
                    user=await profile.user,
                    compare_data_centers=True,
                    compare_schedule=True,
                    check_profile=True,
                    check_nsfw=True,
                    check_genres=self.genres
                )
            ]
        else:
            eligible = [
                profile for profile in self.bot.profile_manager.profiles
                if await self.is_user_eligible(
                    user=await profile.user,
                    compare_data_centers=True,
                    compare_schedule=True,
                    check_profile=True,
                    check_tags=True
                )
            ]
        if not eligible:
            return

        embed = U.make_embed(
            title="Job Posting Alert",
            description=(
                f"An opportunity has been posted for a `{self.position.proper_name}` position at "
                f"`{self.venue.name}`. If you're interested, you can [view the posting "
                f"here]({self.post_url})."
            )
        )

        for profile in eligible:
            try:
                await (await profile.user).send(embed=embed)
            except Exception:
                continue

################################################################################
    def format(self, _name_override: Optional[str] = None, v_name: bool = True) -> str:

        return (
            f"**{_name_override or self.position.proper_name}** " +
            (f"at {self.venue.name}\n" if v_name else "\n") +
            f"**Start:** {U.format_dt(self._start, 'F')}\n"
            f"**End:** {U.format_dt(self._end, 'F')}\n"
        )

################################################################################
    def select_option(self) -> SelectOption:

        hours = round((self._start - datetime.now(UTC)).total_seconds() / 3600)
        days_str = f"{hours // 24} Days and " if hours >= 24 else ""

        return SelectOption(
            label=f"{self.position.proper_name}",
            value=str(self.id),
            description=f"Occurring in {days_str}{hours} Hours",
        )

################################################################################
    async def remove(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Remove Job Posting",
            description=(
                "Are you sure you want to remove this job posting?\n\n"
                
                f"{self.format(None, False)}"
            )
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        if self._candidate.id is not None:
            candidate = await self.candidate
            if candidate is None:
                await self.delete()
                return

            prompt = U.make_embed(
                title="Job Posting Already Accepted",
                description=(
                    "__**This job posting has already been accepted by a candidate.**__\n\n"
                    
                    f"{self.format(None, False)}\n"
                    f"{candidate.mention} ({candidate.display_name})\n\n"
                    
                    "Are you *still* sure you want to remove this job posting?"
                )
            )
            view = ConfirmCancelView(interaction.user)

            await interaction.respond(embed=prompt, view=view)
            await view.wait()

            if not view.complete or view.value is False:
                return

            # If we reach here, the user confirmed the deletion
            notify = U.make_embed(
                title="Job Posting Removed",
                description=(
                    f"The job posting for `{self.position.proper_name}` at "
                    f"`{self.venue.name}` has been removed by the venue owner.\n\n"
                    
                    f"{self.format(None, False)}"
                )
            )
            try:
                await candidate.send(embed=notify)
            except Exception:
                pass

        await self.delete()

################################################################################
    async def set_description(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Job Description",
            attribute="Description",
            cur_val=self.description,
            max_length=250,
            multiline=True
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.description = modal.value
        await self.update_post_components(True)

################################################################################
    async def set_salary(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Job Salary",
            attribute="Salary",
            cur_val=self.salary,
            max_length=50
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.salary = modal.value
        await self.update_post_components(True)

################################################################################
    def time_status(self, time_type: TimeType) -> Embed:

        desc = (
            f"**Current Start Time:** {U.format_dt(self._start, 'f')}\n\n"
        ) if time_type == TimeType.StartTime else (
            f"**Current End Time:** {U.format_dt(self._end, 'f')}\n\n"
        )
        desc += "**Please select the time component you would like to change.**"

        word = "Start" if time_type == TimeType.StartTime else "End"
        return U.make_embed(
            title=f"Change Temporary Job {word} Time",
            description=desc
        )

################################################################################
    def time_menu_status(self) -> Embed:

        return U.make_embed(
            title="Job Posting Time Menu",
            description=(
                f"**Current Start Time:** {U.format_dt(self._start, 'f')}\n"
                f"**Current End Time:** {U.format_dt(self._end, 'f')}\n\n"

                "**You can change the start time, end time, or both.**"
            )
        )

################################################################################
    async def set_schedule(self, interaction: Interaction) -> None:

        prompt = self.time_menu_status()
        view = JobTimeButtonsView(interaction.user, self)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if self._schedule_updated:
            await self.notify_eligible_applicants()
            self._schedule_updated = False

################################################################################
    async def set_both_times(self, interaction: Interaction) -> None:

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
            title=f"Job Posting Start Time",
            description=f"Please select the month this job posting starts in."
        )
        view = FroggeSelectView(interaction.user, Month.select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return None

        month = Month(int(view.value))

        prompt = U.make_embed(
            title=f"Job Posting Start Time",
            description=f"Please select the day this job posting starts on."
        )
        options = [SelectOption(label=str(i), value=str(i)) for i in range(1, month.days() + 1)]
        view = FroggeMultiMenuSelect(interaction.user, options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return None

        day = int(view.value)

        prompt = U.make_embed(
            title=f"Job Posting Start Time",
            description=(
                f"Please select the year of this job posting's start time."
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
            title=f"Job Posting Start Time",
            description=(
                f"Please select the hour, then minute increment of this job posting's "
                f"start time."
            )
        )
        view = TimeSelectView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return None

        hours, minutes = view.value
        start_dt = datetime(
            year=year,
            month=month.value,
            day=day,
            hour=hours,
            minute=minutes,
            tzinfo=tz
        )

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

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        end_dt = start_dt + timedelta(minutes=int(view.value))

        self._set_schedule_impl(start_dt, end_dt)
        await self.update_post_components(True)

################################################################################
    async def poster_left(self) -> None:

        candidate = await self.candidate
        if candidate is not None:
            notify = U.make_embed(
                title="Job Poster Left",
                description=(
                    f"The job poster for `{self.position.proper_name}` at "
                    f"`{self.venue.name}` has left the server.\n\n"
                    
                    f"{self.format(None, False)}\n"
                    "The job posting will now be deleted."
                )
            )
            try:
                await candidate.send(embed=notify)
            except Exception:
                pass

        await self.delete()

################################################################################
    async def time_menu(self, interaction: Interaction, t_type: TimeType) -> None:

        prompt = self.time_status(t_type)
        view = JobTimeComponentView(interaction.user, self, t_type)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

################################################################################
    async def get_tz(self, interaction: Interaction) -> Optional[ZoneInfo]:

        if self._tz is not None:
            return self._tz

        prompt = U.make_embed(
            title=f"Job Posting Timezone",
            description=f"Please select your timezone."
        )
        view = FroggeSelectView(interaction.user, Timezone.select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return None

        self._tz = U.TIMEZONE_OFFSETS[Timezone(int(view.value))]
        return self._tz

################################################################################
    async def set_year(self, interaction: Interaction, t_type: TimeType) -> None:

        tz = await self.get_tz(interaction)
        if tz is None:
            return

        prompt = U.make_embed(
            title="Job Posting Year",
            description="Please select the year for this job posting."
        )
        cur_year = datetime.now().year
        options = [SelectOption(label=str(i), value=str(i)) for i in range(cur_year, cur_year + 2)]
        view = FroggeSelectView(interaction.user, options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        year = int(view.value)
        prev_date = self._start if t_type == TimeType.StartTime else self._end
        new_date = prev_date.astimezone(tz)
        new_date = new_date.replace(year=year)
        if t_type == TimeType.StartTime:
            self._set_schedule_impl(new_date, self._end)
        else:
            self._set_schedule_impl(self._start, new_date)

        await self.update_post_components(True)

################################################################################
    async def set_month(self, interaction: Interaction, t_type: TimeType) -> None:

        tz = await self.get_tz(interaction)
        if tz is None:
            return

        prompt = U.make_embed(
            title="Job Posting Month",
            description="Please select the month for this job posting."
        )
        view = FroggeSelectView(interaction.user, Month.select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        month = Month(int(view.value))
        prev_date = self._start if t_type == TimeType.StartTime else self._end
        new_date = prev_date.astimezone(tz)
        new_date = new_date.replace(month=month.value)
        if t_type == TimeType.StartTime:
            self._set_schedule_impl(new_date, self._end)
        else:
            self._set_schedule_impl(self._start, new_date)

        await self.update_post_components(True)

################################################################################
    async def set_day(self, interaction: Interaction, t_type: TimeType) -> None:

        tz = await self.get_tz(interaction)
        if tz is None:
            return

        prompt = U.make_embed(
            title="Job Posting Day",
            description="Please select the day for this job posting."
        )
        month = Month(self._start.month)
        options = [SelectOption(label=str(i), value=str(i)) for i in range(1, month.days() + 1)]
        view = FroggeMultiMenuSelect(interaction.user, options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        day = int(view.value)
        prev_date = self._start if t_type == TimeType.StartTime else self._end
        new_date = prev_date.astimezone(tz)
        new_date = new_date.replace(day=day)
        if t_type == TimeType.StartTime:
            self._set_schedule_impl(new_date, self._end)
        else:
            self._set_schedule_impl(self._start, new_date)

        await self.update_post_components(True)

################################################################################
    async def set_hour(self, interaction: Interaction, t_type: TimeType) -> None:

        tz = await self.get_tz(interaction)
        if tz is None:
            return

        prompt = U.make_embed(
            title="Job Posting Hour",
            description="Please select the hour for this job posting."
        )
        view = FroggeSelectView(interaction.user, Hours.limited_select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        hour = int(view.value)
        prev_date = self._start if t_type == TimeType.StartTime else self._end
        new_date = prev_date.astimezone(tz)
        new_date = new_date.replace(hour=hour)
        if t_type == TimeType.StartTime:
            self._set_schedule_impl(new_date, self._end)
        else:
            self._set_schedule_impl(self._start, new_date)

        await self.update_post_components(True)

    ################################################################################
    async def set_minute(self, interaction: Interaction, t_type: TimeType) -> None:

        tz = await self.get_tz(interaction)
        if tz is None:
            return

        prompt = U.make_embed(
            title="Job Posting Minute",
            description="Please select the minute for this job posting."
        )
        view = FroggeSelectView(interaction.user, Minutes.select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        minute = Minutes(int(view.value)).value
        prev_date = self._start if t_type == TimeType.StartTime else self._end
        new_date = prev_date.astimezone(tz)
        new_date = new_date.replace(minute=minute)
        if t_type == TimeType.StartTime:
            self._set_schedule_impl(new_date, self._end)
        else:
            self._set_schedule_impl(self._start, new_date)

        await self.update_post_components(True)

################################################################################
