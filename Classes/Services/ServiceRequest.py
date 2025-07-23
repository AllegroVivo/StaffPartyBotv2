from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, List, Dict, Any

from discord import User, Embed, Interaction, SelectOption, Message, ChannelType, HTTPException, EmbedField
from discord.ext.pages import Page

from Assets import BotEmojis
from Classes.Common import ManagedObject, LazyUser, LazyMessage
from UI.Common import FroggeView, FroggeSelectView, BasicTextModal, ConfirmCancelView, RevisitItemView
from Enums import Service, DataCenter, XIVRegion
from UI.Services import ServiceRequestConfirmationView, ServiceRequestAcceptView, ServiceRequestPickupView, ServiceRequestEditView, \
    ServiceRequestStatusView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import ServicesManager
################################################################################

__all__ = ("ServiceRequest", )

SR = TypeVar("SR", bound="ServiceRequest")

################################################################################
class ServiceRequest(ManagedObject):

    __slots__ = (
        "_user",
        "_service",
        "_dc",
        "_description",
        "_budget",
        "_messages",
        "_candidate",
        "_post_message",
    )

################################################################################
    def __init__(self, mgr: ServicesManager, id: int, **kwargs) -> None:

        super().__init__(mgr, id)

        self._user: LazyUser = LazyUser(self, kwargs.pop("user_id"))
        self._service: Service = Service(kwargs.pop("service"))
        self._description: Optional[str] = kwargs.get("description")
        self._budget: Optional[str] = kwargs.get("budget")
        raw_dc = kwargs.get("dc") or kwargs.get("data_center")
        self._dc: Optional[XIVRegion] = XIVRegion(raw_dc) if raw_dc else None

        self._candidate: LazyUser = LazyUser(self, kwargs.get("candidate_id"))
        self._messages = [LazyMessage(self, i) for i in kwargs.get("message_urls", [])]
        self._post_message: LazyMessage = LazyMessage(self, kwargs.get("post_url"))

################################################################################
    @classmethod
    def new(
        cls: Type[SR],
        mgr: ServicesManager,
        user: User,
        service: Service,
        description: Optional[str],
        budget: Optional[str],
        dc: Optional[XIVRegion],
    ) -> SR:

        dc_value = dc.value if dc else None
        new_obj = mgr.bot.db.insert.service_request(user.id, service.value, dc_value, description, budget)
        return cls(
            mgr,
            new_obj["id"],
            user_id=user.id,
            service=service.value,
            description=description,
            budget=budget,
            dc=dc.value if dc is not None else None,
        )

################################################################################
    @property
    async def user(self) -> User:

        return await self._user.get()

    @property
    def user_id(self) -> int:

        return self._user.id
################################################################################
    @property
    def service_type(self) -> Service:

        return self._service

    @service_type.setter
    def service_type(self, value: Service) -> None:

        self._service = value
        self.update()

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
    def budget(self) -> Optional[str]:

        return self._budget

    @budget.setter
    def budget(self, value: Optional[str]) -> None:

        self._budget = value
        self.update()

################################################################################
    @property
    def data_center(self) -> Optional[XIVRegion]:

        return self._dc

    @data_center.setter
    def data_center(self, value: Optional[XIVRegion]) -> None:

        self._dc = value
        self.update()

################################################################################
    @property
    async def blast_messages(self) -> List[Message]:

        return [await msg.get() for msg in self._messages]

    @blast_messages.setter
    def blast_messages(self, value: List[Message]) -> None:

        self._messages = [LazyMessage(self, msg.jump_url) for msg in value]
        self.update()

################################################################################
    @property
    async def post_message(self) -> Optional[Message]:

        return await self._post_message.get()

    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:

        self._post_message.set(value)

################################################################################
    def update(self) -> None:

        self.bot.db.update.service_request(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "service": self._service.value,
            "description": self._description,
            "budget": self._budget,
            "dc": self._dc.value if self._dc is not None else None,
            "message_urls": [msg.url for msg in self._messages],
            "post_url": self._post_message.url if self._post_message else None,
            "candidate_id": self._candidate.id if self._candidate else None,
        }

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.service_request(self.id)
        self._mgr._managed.remove(self)

################################################################################
    async def status(self) -> Embed:

        return U.make_embed(
            title="Service Request Status",
            description=(
                "__**Description:**__\n"
                f"{self._description or '`Not Set`'}"
            ),
            fields=[
                EmbedField(
                    name="__Budget__",
                    value=self._budget or '`Not Set`',
                    inline=True,
                ),
                EmbedField(
                    name="__Data Center__",
                    value=self._dc.proper_name if self._dc is not None else '`Not Set`',
                    inline=True,
                ),
                EmbedField(
                    name="__Current Status__",
                    value=(
                        f"{BotEmojis.CheckGreen} Request Accepted by {(await self.candidate).display_name}"
                        if self.is_accepted else
                        f"{BotEmojis.Cross} Not Accepted Yet!"
                    ),
                    inline=False
                )
            ]
        )
################################################################################
    async def compile(self) -> Embed:

        return U.make_embed(
            title=f"New Request for {self.service_type.proper_name}",
            description=(
                f"**Requesting User:** {(await self.user).mention}\n"
                "__**Description/Details:**__\n"
                f"{self.description or '`No description provided`'}\n\n"
                
                f"**Budget:** {self.budget or '`No budget specified`'}\n"
                f"**Data Center:** `{self.data_center.proper_name if self.data_center else 'Not specified'}`\n\n"

                "Please click the button below to accept this request and "
                "open a private thread with the user to discuss further details."
            )
        )

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        return ServiceRequestStatusView(user, self)

################################################################################
    async def refresh(self) -> None:

        for msg in await self.blast_messages:
            await msg.edit(view=ServiceRequestAcceptView(self))

################################################################################
    async def confirmation_embed(self) -> Embed:

        return U.make_embed(
            title="Service Request Confirmation",
            description=(
                "Please review the details of your service request below.\n\n"
                
                f"**Requesting User:** {(await self.user).mention}\n"
                f"**Service Type:** {self._service.proper_name}\n"
                f"**Description:** {self._description or 'No description provided'}\n"
                f"**Budget:** {self._budget or 'No budget specified'}\n"
                f"**Data Center:** {self._dc.proper_name if self._dc else 'Not specified'}\n"
            ),
        )

################################################################################
    async def confirmation_menu(self, interaction: Interaction) -> None:

        embed = await self.confirmation_embed()
        view = ServiceRequestConfirmationView(interaction.user, self)

        await interaction.respond(view=view, embed=embed)
        await view.wait()

################################################################################
    async def set_service_type(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Modify Service Type",
            description=(
                "Please select the type of service your request will be for.\n\n"
                
                "(This field is __**mandatory**__ to ensure that the request "
                "is properly categorized and directed appropriately.)"
            ),
        )
        view = FroggeSelectView(interaction.user, options=Service.select_options(), show_close=False)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.service_type = Service(int(view.value))
        await self.update_post_components(True)

################################################################################
    async def set_description(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Service Description",
            attribute="Description",
            example="eg. 'I would like to redesign my venue's logo.'",
            cur_val=self.description,
            max_length=500,
            multiline=True
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.description = modal.value
        await self.update_post_components(True)

################################################################################
    async def set_budget(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Service Budget",
            attribute="Budget",
            example="eg. '10.5m or 10,500,000''",
            cur_val=self.budget,
            max_length=100,
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.budget = modal.value
        await self.update_post_components(True)

################################################################################
    async def set_data_center(self, interaction: Interaction) -> None:

        options = XIVRegion.select_options()
        options.append(SelectOption(label="Not Applicable", value="-1"))

        prompt = U.make_embed(
            title="Select Your Data Center",
            description=(
                "Please select the region in which the services will be rendered."
            ),
        )
        view = FroggeSelectView(interaction.user, options=options, show_close=False)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return

        self.data_center = XIVRegion(int(view.value))
        await self.update_post_components(True)

################################################################################
    async def submit(self, interaction: Interaction) -> bool:

        roles = [r for r in interaction.guild.roles if r.name == self.service_type.proper_name]
        if not roles:
            await interaction.respond(
                embed=U.make_error(
                    title="Role Not Found",
                    message="The service type you selected does not have a corresponding role.",
                    solution="Please contact a staff member for assistance."
                ),
                ephemeral=True
            )
            return False

        assert len(roles) == 1, f"Multiple roles found for service type: {self.service_type.proper_name}, this should not happen."

        role = roles[0]
        messages = []
        for member in interaction.guild.members:
            if member == interaction.user:
                continue
            if role in member.roles:
                view = ServiceRequestAcceptView(self)
                messages.append(await member.send(embed=await self.blast_message(), view=view))

        self.blast_messages = messages

        post_channel = await self.bot.channel_manager.services_channel
        if post_channel is None:
            await interaction.respond(
                embed=U.make_error(
                    title="Channel Not Set",
                    message="The services channel is not set. Please contact a staff member.",
                    solution="Your request has been submitted, but no public listing can be posted at this time."
                ),
                ephemeral=True
            )
            return False

        post_view = ServiceRequestPickupView(self)
        pos_thread = next((t for t in post_channel.threads if t.name.lower() == self.service_type.proper_name.lower()), None)
        try:
            if pos_thread is not None:
                self.post_message = await pos_thread.send(embed=await self.compile(), view=post_view)
            else:
                pos_thread = await post_channel.create_thread(name=self.service_type.proper_name, embed=await self.compile(), view=post_view)
                self.post_message = pos_thread.last_message

        except Exception as ex:
            error = U.make_embed(
                title="Posting Error",
                description=f"There was an error posting the service request.\n\n{ex}"
            )
            await interaction.respond(embed=error, ephemeral=True)
        else:
            await self.bot.log.service_request_posted(self)

        return True

################################################################################
    async def blast_message(self, completed: bool = False) -> Embed:

        # Try to get the SPB member so we can attach their display name
        # (i.e., character name) to the message.
        member = await self.bot.get_or_fetch_member_or_user(self._user.id)
        phrase = (
            "Please click the 'Accept' button below to pick up this request and "
            "open a private thread with the user to discuss further details."
            if not completed else
            "***This request has been completed and is no longer active.***"
        )
        return U.make_embed(
            title="Service Request Submitted",
            description=(
                "A new service request has been submitted. Please review the "
                "details below and respond accordingly.\n\n"
                
                f"**Service Type:** {self._service.proper_name}\n"
                f"**Description:** {self._description or 'No description provided'}\n"
                f"**Budget:** {self._budget or 'No budget specified'}\n"
                f"**Data Center:** {self._dc.proper_name if self._dc else 'Not specified'}\n\n"
                
                f"**Requesting User:** {member.display_name}\n"
                f"{U.draw_line(extra=30)}\n"              
                f"{phrase}"
            )
        )

################################################################################
    async def accept(self, interaction: Interaction) -> None:

        await interaction.response.defer(invisible=False, ephemeral=True)

        self.candidate = interaction.user
        u1 = await self.user
        u2 = interaction.user

        services_channel = await self.bot.channel_manager.communication_channel
        thread = await services_channel.create_thread(
            name=f"Service Request: {u1.display_name} - {self.service_type.proper_name}",
            type=ChannelType.private_thread
        )
        await thread.add_user(u1)
        await thread.add_user(u2)
        await thread.send(
            f"Hello {u1.mention} & {u2.mention},\n\n"
            "Thank you for your service request! "
            "I've opened this private thread to discuss further details and arrange the service."
        )

        embed = U.make_embed(
            title="Service Request Accepted",
            description=(
                f"You've accepted the service request for a "
                f"`{self.service_type.proper_name}`.\n\n"
                
                "I've opened a private thread with the user to discuss further details "
                "and arrange the service.\n\n"
                
                f"Click here to go there now: {thread.jump_url}"
            ),
        )
        await interaction.respond(embed=embed, ephemeral=True)

        for msg in await self.blast_messages:
            await msg.edit(embed=await self.blast_message(completed=True), view=None)

        self.blast_messages = []
        await self.update_post_components(True)

        self.register_revisit_timer()

################################################################################
    async def decline(self, interaction: Interaction) -> None:

        embed = U.make_embed(
            title="Thank You for Your Consideration",
            description=(
                f"You've decided to decline the service request for a "
                f"`{self.service_type.proper_name}` at this time.\n\n"
                
                "If you want to fully opt-out of messages like this in the future, "
                "please visit the Staff Party bus discord to remove your "
                f"{self.service_type.proper_name} role."
            ),
        )
        await interaction.respond(embed=embed, ephemeral=True)
        await interaction.message.edit(view=None)

################################################################################
    async def update_post_components(
        self,
        update_status: bool = False,
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

        view = ServiceRequestPickupView(self)
        self.bot.add_view(view, message_id=self._post_message.id)

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
    async def cancel(self, interaction: Optional[Interaction] = None) -> None:

        candidate = await self.candidate
        if candidate is None:
            return

        # Log before removing the candidate
        await self.bot.log.service_canceled(self)

        self.candidate = None
        await self.update_post_components(True)

        if interaction is not None:
            await interaction.edit()

        notify = U.make_embed(
            title="Service Request Canceled",
            description=(
                f"__**Request Details**__\n\n"
                f"`{self.service_type.proper_name}`\n"
                f"*({self.description or '`No Description Provided`'})*\n\n"

                "The previous candidate has removed themself from this service request.\n\n"

                "For your convenience, the posting has been re-activated and "
                "is now available for other applicants to accept."
            )
        )

        try:
            to_notify = await self.user
            await to_notify.send(embed=notify)
        except Exception:
            pass

################################################################################
    async def page(self) -> Page:

        status = (
            f"{BotEmojis.Check} Accepted by\n`{(await self.candidate).display_name}`"
            if self.is_accepted else
            f"{BotEmojis.Cross} `Not Accepted Yet`"
        )
        return Page(
            embeds=[
                U.make_embed(
                    title=f"Service Request: {self.service_type.proper_name}",
                    description=(
                        f"{status}\n\n"
                        
                        f"**Description:**\n"
                        f"{self.description or '`No description provided`'}\n\n"
                        
                        f"**Budget:** {self.budget or '`No budget specified`'}\n\n"
                        
                        f"**Data Center:** `{self.data_center.proper_name if self.data_center else 'Not specified'}`\n\n"
                        
                        "Please click any of the buttons below to "
                        "perform actions on this service request."
                    )
                )
            ],
            custom_view=ServiceRequestEditView(self)
        )

################################################################################
    async def remove(self, interaction: Interaction) -> bool:

        prompt = U.make_embed(
            title=f"Remove ",
            description=f"Are you sure you want to remove this service request?"
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return False

        post_message = await self.post_message
        if post_message is not None:
            try:
                await post_message.delete()
            except:
                pass

        self.delete()
        return True

################################################################################
    def register_revisit_timer(self) -> None:

        self._mgr.register_revisit(self)  # type: ignore

################################################################################
    async def revisit(self) -> None:

        prompt = U.make_embed(
            title="Just Checking In!",
            description=(
                "It's been a while since the following service request was created "
                "and accepted by a candidate.\n\n"

                f"__**Service Requested:**__ {self.service_type.proper_name}\n"
                f"__**Description:**__\n"
                f"{self.description or '`No description provided`'}\n\n"
                
                f"__**Budget:**__ {self.budget or '`No budget specified`'}\n\n"
                
                f"__**Data Center:**__ {self._dc.proper_name if self._dc is not None else '`Not Provided`'}\n\n"

                "Please take a moment to select one of the following buttons, "
                "indicating whether the candidate worked out or not.\n\n"

                "If the candidate was a good match, the job posting will be "
                "removed from SPB. If not, it will be automatically re-activated "
                "for other candidates to apply to."
            )
        )
        view = RevisitItemView(self)

        posting_user = await self.user
        assert posting_user is not None, "Posting user is None"

        await posting_user.send(embed=prompt, view=view)

################################################################################