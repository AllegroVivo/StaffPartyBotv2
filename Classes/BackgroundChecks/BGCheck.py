from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Any, Dict

from discord import User, Embed, Interaction, EmbedField, Message

from Classes.Common import LazyUser, LazyMessage, LazyRole
from UI.BackgroundChecks import BGCheckMenuView, BGCheckVenueModal, DataCenterWorldSelectView
from UI.Common import (
    BasicTextModal,
    InstructionsInfo,
    FroggeSelectView,
    ConfirmCancelView
)

from .BGCheckVenue import BGCheckVenue
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import BGCheckManager, StaffPartyBot
################################################################################

__all__ = ("BGCheck", )

################################################################################
class BGCheck:

    __slots__ = (
        "_id",
        "_mgr",
        "_user",
        "_agree",
        "_names",
        "_venues",
        "_approved",
        "_post_msg",
        "_submitted",
        "_approved_at",
        "_approved_by",
    )

################################################################################
    def __init__(self, mgr: BGCheckManager, id: int, **kwargs) -> None:

        self._id: int = id
        self._mgr: BGCheckManager = mgr
        self._user: LazyUser = LazyUser(self, kwargs.get("user_id"))

        self._names: List[str] = kwargs.get("names", [])
        self._agree: bool = kwargs.get("agree", False)
        self._approved: bool = kwargs.get("approved", False)

        self._venues: List[BGCheckVenue] = [BGCheckVenue(**v) for v in kwargs.get("venues", [])]
        self._post_msg: LazyMessage = LazyMessage(self, kwargs.get("post_url"))

        self._submitted: Optional[datetime] = kwargs.get("submitted_at")
        self._approved_at: Optional[datetime] = kwargs.get("approved_at")
        self._approved_by: LazyUser = LazyUser(self, kwargs.get("approved_by"))

################################################################################
    @classmethod
    def new(cls, mgr: BGCheckManager, user: User) -> BGCheck:

        new_data = mgr.bot.db.insert.bg_check(user.id)
        return cls(mgr, **new_data)

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._mgr.bot

################################################################################
    @property
    def id(self) -> int:

        return self._id

################################################################################
    @property
    async def user(self) -> User:

        return await self._user.get()

    @property
    def user_id(self) -> int:

        return self._user.id

################################################################################
    @property
    def names(self) -> List[str]:

        return sorted(self._names)

    @names.setter
    def names(self, value: List[str]) -> None:

        self._names = value
        self.update()

################################################################################
    @property
    def venues(self) -> List[BGCheckVenue]:

        return sorted(self._venues, key=lambda v: v.name.lower())

################################################################################
    @property
    def is_submitted(self) -> bool:

        return self._submitted is not None

################################################################################
    @property
    def approved(self) -> bool:

        return self._approved

    @approved.setter
    def approved(self, value: bool) -> None:

        self._approved = value
        self.update()

################################################################################
    @property
    async def post_message(self) -> Optional[Message]:

        return await self._post_msg.get()

    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:

        self._post_msg.set(value)

################################################################################
    @property
    async def approved_by(self) -> Optional[User]:

        return await self._approved_by.get()

################################################################################
    def update(self) -> None:

        self.bot.db.update.bg_check(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "names": self._names,
            "agree": self._agree,
            "approved": self._approved,
            "post_url": self._post_msg.id,
            "submitted_at": self._submitted,
            "approved_at": self._approved_at,
            "approved_by": self._approved_by.id,
        }

################################################################################
    def status(self) -> Embed:

        return U.make_embed(
            title="Background Check",
            description=(
                "If you have no experience in a venue, please close this\n"
                "message and select 'Desired Trainings' from the previous menu.\n\n"
                
                "__**Please read, and either agree or disagree to the "
                "following:**__\n"
                "> *I confirm that the information I provide in this background\n"
                "> check is true and I also provide consent to the employees\n"
                "> of the Staff Party Bus to contact and verify my references.*\n\n"

                "Please note that it is __**OKAY**__ to disagree with the above\n"
                "statement. If you do, a staff member will contact you shortly.\n\n"
                
                "If you have never worked in a venue, you must receive training to\n"
                "become qualified. If you've just received training, please list that!\n"
                f"{U.draw_line(extra=36)}"
            ),
            fields=[
                EmbedField(
                    name="__Character Names__",
                    value=(
                        "\n".join([f"- `{n}`" for n in self.names])
                        if self._names else "`No Names Provided`"
                    ),
                    inline=False
                ),
                EmbedField(
                    name="__Previous Venues__",
                    value=(
                        "\n".join([f"- {v.format()}" for v in self.venues])
                        if self._venues else "`No Venue Information Provided`"
                    ),
                    inline=False
                )
            ]
        )

################################################################################
    async def menu(self, interaction: Interaction) -> None:

        embed = self.status()
        view = BGCheckMenuView(interaction.user, self)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    async def set_names(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Character Names",
            attribute="Name(s)",
            cur_val=", ".join(self.names),
            example="eg. 'Allegro Vivo'",
            max_length=200,
            multiline=True,
            instructions=InstructionsInfo(
                placeholder="Enter your character name(s).",
                value=(
                    "Please enter the name(s) of your game character(s).\n"
                    "Separate names with a comma - eg. 'Allegro Vivo, Vivace Vivo'."
                )
            )
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.names = [n.strip() for n in modal.value.split(",")]

################################################################################
    async def add_venue(self, interaction: Interaction) -> None:

        assert len(self.venues) < 3, "Cannot have more than 3 venues."

        modal = BGCheckVenueModal()

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        name, jobs = modal.value

        prompt = U.make_embed(
            title="Select Data Center & World",
            description=(
                "Please select the data center and world where this venue "
                "was located"
            )
        )
        view = DataCenterWorldSelectView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        data_center, world = view.value

        matching_venues = [v for v in self.venues if v.name.lower() == name.lower()]
        if matching_venues:
            error = U.make_error(
                title="Job Experience Already Exists",
                message=f"Experience for {name} already exists.",
                solution="Please remove the existing experience before adding a new one."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        venue = BGCheckVenue.new(self, name, data_center, world, jobs)
        self._venues.append(venue)

################################################################################
    async def remove_venue(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Remove Venue",
            description="Please select the venue you would like to remove."
        )
        view = FroggeSelectView(interaction.user, [v.select_option() for v in self.venues])

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        venue = next((v for v in self.venues if v.name == view.value))
        if await venue.remove(interaction):
            self._venues.remove(venue)

################################################################################
    async def submit(self, interaction: Interaction, agreed: bool) -> bool:

        if not self.names:
            error = U.make_error(
                title="Missing Name",
                message="You must provide at least one character name to continue.",
                solution="Enter your character name(s) and try again."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return False

        word = "AGREE" if agreed else "DISAGREE"
        prompt = U.make_embed(
            title="Submit and Agree",
            description=(
                "Are you sure you want to submit your background check\n"
                f"and __**{word}**__ to the above-mentioned terms?"
            )
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return False

        # Setting the post_message property will call update for all of these attributes
        self._agree = agreed
        self._submitted = datetime.now()
        self.post_message = await self.bot.log.bg_check_submitted(self)

        if agreed:
            description = (
                "Your background check has been submitted!\n"
                "You will receive a DM from the bot letting you\n"
                "know when you've been approved.\n\n"
                
                "You may not select your qualified positions until\n"
                "your approval is processed."
            )
        else:
            description = (
                "Your background check has been submitted.\n"
                "You will be contacted by a staff member shortly.\n\n"

                "You may not select your qualified positions until\n"
                "your approval is processed."
            )

        confirm = U.make_embed(
            title="Background Check Submitted",
            description=description,
            timestamp=True
        )

        await interaction.respond(embed=confirm, ephemeral=True)
        return True

################################################################################
    async def approve(self, approved_by: User) -> None:

        if self.approved:
            return

        bg_check_user = await self.user
        await self.bot.role_manager.approve_staff(bg_check_user)  # type: ignore

        self._approved_at = datetime.now()
        self._approved_by = LazyUser(self, approved_by.id)
        self.approved = True

        confirm = U.make_embed(
            title="Approved",
            description=(
                "Your background check has been approved!\n\n"
                
                "You now have access to the `Qualified Positions` button on your "
                "staff profile!"
            )
        )
        try:
            await bg_check_user.send(embed=confirm)
        except:
            pass

        await self.bot.log.bg_check_approved(self)

################################################################################
    async def staff_experience(self, interaction: Interaction) -> None:

        await interaction.respond(embed=await self.detail_status())

################################################################################
    async def detail_status(self) -> Embed:

        ret = self.status()
        ret.description = "For: " + (await self.user).mention
        ret.fields.extend([
            EmbedField(
                name="__Submitted At__",
                value=(
                    U.format_dt(self._submitted, "F")
                    if self._submitted is not None
                    else "`Not Submitted`"
                ),
                inline=False
            ),
            EmbedField(
                name="__Approved At__",
                value=(
                    f"{U.format_dt(self._approved_at, 'F')}\n"
                    f"by {(await self.approved_by).mention}"
                ) if self._approved_at is not None else "`Not Approved`",
                inline=False
            ),
        ])

        return ret

################################################################################
