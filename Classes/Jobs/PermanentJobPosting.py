from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Type, Optional, Any, Dict, List

from Assets import BotEmojis
from Classes.Common import Identifiable, LazyUser, LazyMessage

from discord import Embed, User, Message, Interaction, ForumChannel, EmbedField, HTTPException, Thread, ChannelType
from Enums import Position, Weekday
from UI.Common import ConfirmCancelView, BasicTextModal, RevisitItemView
from UI.Jobs import PermanentJobPostingStatusView, JobPostingPickupView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import JobPostingManager, Venue, StaffPartyBot
################################################################################

__all__ = ("PermanentJobPosting", )

PJP = TypeVar("PJP", bound="PermanentJobPosting")

################################################################################
class PermanentJobPosting(Identifiable):

    __slots__ = (
        "_mgr",
        "_user",
        "_venue_id",
        "_position",
        "_salary",
        "_description",
        "_post_msg",
        "_candidate"
    )

################################################################################
    def __init__(self, mgr: JobPostingManager, id: int, **kwargs) -> None:

        super().__init__(id)

        self._mgr: JobPostingManager = mgr

        self._user: LazyUser = LazyUser(self, kwargs.pop("user_id"))
        self._venue_id: int = kwargs.pop("venue_id")
        self._position: Position = Position(kwargs.pop("position_id"))
        self._salary: Optional[str] = kwargs.get("salary")
        self._description: str = kwargs.pop("description")
        self._post_msg: LazyMessage = LazyMessage(self, kwargs.get("post_url"))
        self._candidate: LazyUser = LazyUser(self, kwargs.get("candidate_id"))


################################################################################
    @classmethod
    def new(
        cls: Type[PJP],
        mgr: JobPostingManager,
        venue: Venue,
        user: User,
        position: Position,
        descr: str,
        salary: Optional[str]
    ) -> PJP:

        new_data = mgr.bot.db.insert.permanent_job(
            venue.id, user.id, position.value, descr, salary
        )
        return cls(mgr, **new_data)

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._mgr.bot

################################################################################
    @property
    async def user(self) -> User:

        return await self._user.get()

################################################################################
    @property
    def position(self) -> Position:

        return self._position

################################################################################
    @property
    async def post_message(self) -> Optional[Message]:

        return await self._post_msg.get()

    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:

        self._post_msg.set(value)

    @property
    def post_url(self) -> Optional[str]:

        return self._post_msg.url

################################################################################
    @property
    def venue(self) -> Venue:

        return self.bot.venue_manager[self._venue_id]

################################################################################
    @property
    async def post_channel(self) -> Optional[ForumChannel]:

        return await self.bot.channel_manager.perm_jobs_channel

################################################################################
    @property
    def description(self) -> str:

        return self._description

    @description.setter
    def description(self, value: str) -> None:

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
    async def candidate(self) -> Optional[User]:

        return await self._candidate.get()

    @candidate.setter
    def candidate(self, value: Optional[User]) -> None:

        self._candidate.set(value)

################################################################################
    @property
    async def posting_user(self) -> User:

        return await self._user.get()

################################################################################
    def update(self) -> None:

        self.bot.db.update.permanent_job(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "description": self._description,
            "salary": self._salary,
            "post_url": self.post_url,
            "candidate_id": self._candidate.id if self._candidate else None,
        }

################################################################################
    async def delete(self) -> None:

        self.bot.db.delete.permanent_job(self.id)

        post_message = await self.post_message
        if post_message:
            try:
                await post_message.delete()
            except Exception as e:
                print(e)

        for i, timer in enumerate(self._mgr._revisits):
            if timer.context == self:
                self._mgr._revisits.pop(i)
                break

        self._mgr._permanent.remove(self)

################################################################################
    def format(self, _name_override: Optional[str] = None, v_name: bool = True) -> str:

        return (
            f"**{_name_override or self.position.proper_name}** " +
            (f"at {self.venue.name}" if v_name else "")
        )

################################################################################
    def status(self) -> Embed:

        return U.make_embed(
            title=f"Job Posting Status",
            description=(
                "__**Venue Name:**__\n"
                f"`{self.venue.name}`\n\n"

                "__**Job Description:**__\n"
                f"{U.wrap_text(self._description or '`No Description`', 50)}\n\n"

                f"{U.draw_line(extra=30)}\n"
            ),
            fields=[
                EmbedField(
                    name="__Position__",
                    value=f"`{self._position.proper_name}`",
                    inline=False
                ),
                EmbedField(
                    name="__Salary Info__",
                    value=f"`{self._salary}`" if self.salary is not None else "`Not Provided`",
                    inline=False
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

        embed = self.status()
        view = PermanentJobPostingStatusView(interaction.user, self)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    async def compile(self) -> Embed:

        managers = await self.venue.managers
        manager_str = "\n".join([f"- {m.mention} ({m.display_name})" for m in managers])
        hours_value = (
            "\n".join([f"- {h.format()}" for h in self.venue.schedule])
        ) if self.venue.schedule else "`No Schedule Provided`"

        return U.make_embed(
            title=f"`{self.position.proper_name}` Needed at `{self.venue.name}`",
            description=(
                "__**Venue Contacts:**__\n"
                f"{manager_str}\n\n"
    
                "__**Venue Details:**__\n"
                f"`{self.venue.location.format()}`\n\n"
                
                "__**Venue Hours:**__\n"
                f"{hours_value}\n\n"
    
                "__Venue Profile:__\n"
                f"[Click here to view the venue profile]({self.venue.post_url})\n\n"
    
                "__**Job Description:**__\n"
                f"{U.wrap_text(self._description, 50)}\n"
    
                f"{U.draw_line(extra=30)}\n"
            ),
            fields=[
                EmbedField(
                    name="__Position__",
                    value=f"`{self.position.proper_name}`",
                    inline=True
                ),
                EmbedField(
                    name="__Salary__",
                    value=f"`{self._salary}`" if self.salary is not None else "`Not Provided`",
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

        # We should be able to use the same type of View here as long as this
        # class implements the `candidate_accept` and `cancel` methods.
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
            print(ex)
            await interaction.respond(embed=error, ephemeral=True)
        else:
            await self.bot.log.perm_job_posted(self)

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
        assert self._post_msg.id is not None, "Post message ID is None"
        msg_id = self._post_msg.id.split("/")[-1]
        self.bot.add_view(view, message_id=int(msg_id))

        try:
            if update_view and not update_status:
                await post_message.edit(view=view)
                pass
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
    async def set_description(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Job Posting Description",
            attribute="Description",
            cur_val=self._description,
            max_length=500
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.description = modal.value
        await self.update_post_components(True, True)

################################################################################
    async def set_salary(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Job Posting Salary",
            attribute="Salary",
            cur_val=self._salary,
            max_length=200,
            required=False
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.salary = modal.value
        await self.update_post_components(True, True)

################################################################################
    async def candidate_accept(self, interaction: Interaction) -> None:

        if not await self.is_user_eligible(interaction.user, True):
            error = U.make_error(
                title="Ineligible for Job",
                message="You are not eligible for this job.",
                solution=(
                    "Please ensure that your staff profile has been "
                    "completed and posted!\n"
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
        self.register_revisit_timer()

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
    async def cancel(self, interaction: Interaction) -> None:

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
    async def is_user_eligible(self, user: User, check_profile: bool = False) -> bool:

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

        # If none of the above conditions matched, the user is eligible
        return True

################################################################################
    async def revisit(self) -> None:

        prompt = U.make_embed(
            title="Just Checking In!",
            description=(
                "It's been a while since the following job posting was created and "
                "accepted by a candidate.\n\n"
                
                f"{self.format(None, False)}\n\n"
                
                "Please take a moment to select one of the following buttons, "
                "indicating whether the candidate worked out or not.\n\n"
                
                "If the candidate was a good match, the job posting will be "
                "removed from SPB. If not, it will be automatically re-activated "
                "for other candidates to apply to."
            )
        )
        view = RevisitItemView(self)

        posting_user = await self.posting_user
        assert posting_user is not None, "Posting user is None"

        await posting_user.send(embed=prompt, view=view)

################################################################################
    def register_revisit_timer(self) -> None:

        self._mgr.register_revisit(self)

################################################################################