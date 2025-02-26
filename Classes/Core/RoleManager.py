from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from discord import Role, Embed, EmbedField, Interaction, SelectOption, Member, User

from Classes.Common import LazyRole
from Enums import RoleType
from UI.Common import FroggeMultiMenuSelect
from UI.Core import RoleManagerMenuView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("RoleManager", )

################################################################################
class RoleManager:

    __slots__ = (
        "_state",
        "_staff_main",
        "_staff_unvalidated",
        "_venue_management",
        "_trainee",
        "_trainee_hiatus"
    )

################################################################################
    def __init__(self, state: StaffPartyBot) -> None:

        self._state: StaffPartyBot = state

        self._staff_main: LazyRole = LazyRole(self, None)
        self._staff_unvalidated: LazyRole = LazyRole(self, None)
        self._venue_management: LazyRole = LazyRole(self, None)
        self._trainee: LazyRole = LazyRole(self, None)
        self._trainee_hiatus: LazyRole = LazyRole(self, None)

################################################################################
    def load_all(self, payload: Dict[str, Any]) -> None:

        self._staff_main = LazyRole(self, payload.get("staff_role_id"))
        self._staff_unvalidated = LazyRole(self, payload.get("staff_pending_role_id"))
        self._venue_management = LazyRole(self, payload.get("venue_management_role_id"))
        self._trainee = LazyRole(self, payload.get("trainee_role_id"))
        self._trainee_hiatus = LazyRole(self, payload.get("trainee_hiatus_role_id"))

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._state

################################################################################
    @property
    async def staff_main_role(self) -> Optional[Role]:

        return await self._staff_main.get()

################################################################################
    @property
    async def staff_pending_role(self) -> Optional[Role]:

        return await self._staff_unvalidated.get()

################################################################################
    @property
    async def venue_management_role(self) -> Optional[Role]:

        return await self._venue_management.get()

################################################################################
    @property
    async def trainee_role(self) -> Optional[Role]:

        return await self._trainee.get()

################################################################################
    @property
    async def trainee_hiatus_role(self) -> Optional[Role]:

        return await self._trainee_hiatus.get()

################################################################################
    def update(self) -> None:

        self.bot.db.update.top_level(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "staff_role_id": self._staff_main.id,
            "staff_pending_role_id": self._staff_unvalidated.id,
            "venue_management_role_id": self._venue_management.id,
            "trainee_role_id": self._trainee.id,
            "trainee_hiatus_role_id": self._trainee_hiatus.id
        }

################################################################################
    async def status(self) -> Embed:

        staff_role = await self.staff_main_role
        staff_pending_role = await self.staff_pending_role
        venue_management_role = await self.venue_management_role
        trainee_role = await self.trainee_role
        trainee_hiatus_role = await self.trainee_hiatus_role

        return U.make_embed(
            title="TrainerBot Roles Status",
            description=U.draw_line(extra=25),
            fields=[
                EmbedField(
                    name="__Staff__",
                    value=staff_role.mention if staff_role else "`Not Set`",
                    inline=False
                ),
                EmbedField(
                    name="__Staff Pending__",
                    value=staff_pending_role.mention if staff_pending_role else "`Not Set`",
                    inline=False
                ),
                EmbedField(
                    name="__Venue Management__",
                    value=venue_management_role.mention if venue_management_role else "`Not Set`",
                    inline=False
                ),
                EmbedField(
                    name="__Trainee__",
                    value=trainee_role.mention if trainee_role else "`Not Set`",
                    inline=False
                ),
                EmbedField(
                    name="__Trainee Hiatus__",
                    value=trainee_hiatus_role.mention if trainee_hiatus_role else "`Not Set`",
                    inline=False
                )
            ]
        )

################################################################################
    async def main_menu(self, interaction: Interaction) -> None:

        embed = await self.status()
        view = RoleManagerMenuView(interaction.user, self)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    def get_role(self, rtype: RoleType) -> LazyRole:

        match rtype:
            case RoleType.StaffMain:
                return self._staff_main
            case RoleType.StaffNotValidated:
                return self._staff_unvalidated
            case RoleType.VenueManagement:
                return self._venue_management
            case RoleType.Trainee:
                return self._trainee
            case RoleType.TraineeHiatus:
                return self._trainee_hiatus
            case _:
                raise ValueError(f"Invalid RoleType: {rtype}")

################################################################################
    async def set_role(self, interaction: Interaction, _type: RoleType) -> None:

        prompt = U.make_embed(
            title="Role Update",
            description=f"Please select the role you would like to set as the `{_type.proper_name}`."
        )
        options = [
            SelectOption(label=r.name, value=str(r.id))
            for r in sorted(interaction.guild.roles, key=lambda r: r.position)
            if r.name != "@everyone"
        ]
        view = FroggeMultiMenuSelect(interaction.user, options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is None:
            return

        role = interaction.guild.get_role(int(view.value))

        match _type:
            case RoleType.StaffMain:
                self._staff_main.set(role)
            case RoleType.StaffNotValidated:
                self._staff_unvalidated.set(role)
            case RoleType.VenueManagement:
                self._venue_management.set(role)
            case RoleType.Trainee:
                self._trainee.set(role)
            case RoleType.TraineeHiatus:
                self._trainee_hiatus.set(role)
            case _:
                raise ValueError(f"Invalid RoleType: {_type}")

################################################################################
    async def _add_role(self, user: Member, _type: RoleType) -> None:

        if isinstance(user, User):
            guild = self.bot.get_guild(self.bot.SPB_ID)
            user = guild.fetch_member(user.id)

        role = await self.get_role(_type).get()
        if role is None:
            return

        if role not in user.roles:
            try:
                await user.add_roles(role)
            except Exception as ex:
                print(f"Failed to add role {role.name} to {user.name}\n", ex)

################################################################################
    async def _remove_role(self, user: Member, _type: RoleType) -> None:

        if isinstance(user, User):
            guild = self.bot.get_guild(self.bot.SPB_ID)
            user = guild.fetch_member(user.id)

        role = await self.get_role(_type).get()
        if role is None:
            return

        if role in user.roles:
            try:
                await user.remove_roles(role)
            except Exception as ex:
                print(f"Failed to remove role {role.name} from {user.name}\n", ex)

################################################################################
    async def approve_staff(self, user: Member) -> None:

        await self._add_role(user, RoleType.StaffMain)
        await self._remove_role(user, RoleType.StaffNotValidated)

################################################################################
