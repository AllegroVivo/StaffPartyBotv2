from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Type, Optional, Any, Dict

from Assets import BotEmojis
from Classes.Common import Identifiable, LazyUser, LazyMessage

from discord import Embed, User, Message, Interaction, ForumChannel, EmbedField, HTTPException
from Enums import Position
from UI.Common import ConfirmCancelView, BasicTextModal
from UI.Jobs import PermanentJobPostingStatusView
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
    def update(self) -> None:

        self.bot.db.update.permanent_job(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "description": self._description,
            "salary": self._salary,
            "post_url": self.post_url
        }

################################################################################
    async def delete(self) -> None:

        self.bot.db.delete.permanent_job(self.id)

        post_message = await self.post_message
        if post_message:
            try:
                await post_message.delete()
            except Exception:
                pass

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
                    value=self._salary,
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

        return U.make_embed(
            title=f"`{self.position.proper_name}` Needed at `{self.venue.name}`",
            description=(
                "__**Venue Contacts:**__\n"
                f"{manager_str}\n\n"
    
                "__**Venue Address:**__\n"
                f"`{self.venue.location.format()}`\n\n"
    
                "__**Job Description:**__\n"
                f"{U.wrap_text(self._description, 50)}\n"
    
                f"{U.draw_line(extra=30)}\n"
            ),
            fields=[
                EmbedField(
                    name="__Position__",
                    value=f"`{self.position.proper_name}`",
                    inline=False
                ),
                EmbedField(
                    name="__Salary__",
                    value=self._salary,
                    inline=False
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
        # post_view = JobPostingPickupView(self)
        # self.bot.add_view(post_view)

        pos_thread = next((t for t in channel.threads if t.name.lower() == self.position.proper_name.lower()), None)
        try:
            if pos_thread is not None:
                self.post_message = await pos_thread.send(embed=await self.compile())  # , view=post_view)
            else:
                pos_thread = await channel.create_thread(name=self.position.proper_name, embed=await self.compile())  # , view=post_view)
                self.post_message = pos_thread.last_message

            confirm = U.make_embed(
                title="Permanent Job Posting Created",
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
            await self.bot.log.perm_job_posted(self)
            # await self.notify_eligible_applicants()

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

        # view = JobPostingPickupView(self)
        # self.bot.add_view(view, message_id=self._post_msg.id)

        try:
            if update_view and not update_status:
                # await post_message.edit(view=view)
                pass
            else:
                await post_message.edit(embed=await self.compile())  # , view=view)
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
