from __future__ import annotations

from datetime import datetime, UTC
from zoneinfo import ZoneInfo
from typing import TYPE_CHECKING, Optional, Type, TypeVar

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
from Enums import Weekday, Position
from UI.Jobs import JobPostingPickupView, TemporaryJobPostingStatusView
from Utilities import Utilities as U
from UI.Common import ConfirmCancelView

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
        self._post_msg: LazyMessage = LazyMessage(self, kwargs.get("post_url"))

        self._salary: str = kwargs.get("salary")
        self._start: datetime = kwargs.get("start_dt").replace(tzinfo=ZoneInfo("UTC"))
        self._end: datetime = kwargs.get("end_dt").replace(tzinfo=ZoneInfo("UTC"))

        self._schedule_updated: bool = False

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
        end_dt: datetime
    ) -> JP:

        new_data = mgr.bot.db.insert.temporary_job(
            venue_id=venue.id,
            user_id=user.id,
            position_id=position.value,
            description=description,
            salary=salary,
            start_dt=start_dt,
            end_dt=end_dt
        )
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

################################################################################
    @property
    def position(self) -> Position:

        return self._position

################################################################################
    @property
    def venue(self) -> Venue:

        return self.bot.venue_manager[self._venue_id]

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

        return U.make_embed(
            title=f"`{self.position.proper_name}` Needed at `{self.venue.name}`",
            description=description,
            fields=[
                EmbedField(
                    name="__Position__",
                    value=f"`{self.position.proper_name}`",
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
            ],
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

            confirm = U.make_embed(
                title="Temporary Job Posting Created",
                description=f"The job posting has been created."
            )
            await interaction.respond(embed=confirm, ephemeral=True)
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
    ) -> bool:

        # Check user and venue mute lists
        if user in await self.venue.muted_users:
            return False

        profile = self.bot.profile_manager.get_profile(user.id)
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
    async def candidate_accept(self, interaction: Interaction) -> None:

        if not await self.is_user_eligible(
            interaction.user,
            compare_data_centers=False,
            compare_schedule=False,
            check_profile=True,
            check_nsfw=False,
            check_tags=False
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

        await self.bot.log.temp_job_accepted(self)

################################################################################
    async def _open_thread(self, interaction: Interaction) -> Optional[Thread]:

        parent_channel = await self.bot.channel_manager.internship_channel
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
        await self.bot.log.temp_job_canceled(self)

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

        await self.delete()

################################################################################
