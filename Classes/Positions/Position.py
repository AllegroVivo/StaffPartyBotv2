from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List, Dict, Any, Type, TypeVar

from discord import User, Embed, Role, EmbedField, Interaction, SelectOption

from Classes.Common import ManagedObject, LazyRole
from Errors import MaxItemsReached
from UI.Positions import PositionStatusView
from Utilities import Utilities as U
from UI.Common import BasicTextModal, FroggeMultiMenuSelect

if TYPE_CHECKING:
    from Classes import PositionManager, Requirement
    from UI.Common import FroggeView
################################################################################

__all__ = ("Position", )

P = TypeVar("P", bound="Position")

################################################################################
class Position(ManagedObject):

    __slots__ = (
        "_name",
        "_requirements",
        "_role",
        "_description",
    )

################################################################################
    def __init__(self, mgr: PositionManager, id: int, **kwargs) -> None:

        super().__init__(mgr, id)

        self._name: Optional[str] = kwargs.get("name")
        self._requirements: List[Requirement] = kwargs.get("requirements", [])
        self._role: LazyRole = LazyRole(self, kwargs.get("role_id"))
        self._description: Optional[str] = kwargs.get("description")

################################################################################
    @classmethod
    def new(cls: Type[P], mgr: PositionManager, name: str) -> P:

        new_data = mgr.bot.db.insert.position(name)
        return cls(mgr, new_data["id"], name=name)

################################################################################
    @property
    def name(self) -> Optional[str]:

        return self._name

    @name.setter
    def name(self, value: str) -> None:

        self._name = value
        self.update()

################################################################################
    @property
    def requirements(self) -> List[Requirement]:

        return self._requirements

    @requirements.setter
    def requirements(self, value: List[Requirement]) -> None:

        self._requirements = value
        self.update()

################################################################################
    @property
    async def role(self) -> Role:

        return await self._role.get()

    @role.setter
    def role(self, value: Optional[Role]) -> None:

        self._role.set(value)

################################################################################
    @property
    def description(self) -> Optional[str]:

        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:

        self._description = value
        self.update()

################################################################################
    def update(self) -> None:

        self.bot.db.update.position(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "name": self._name,
            "role_id": self._role.id,
            "description": self._description,
            "requirement_ids": [req.id for req in self._requirements],
        }

################################################################################
    async def status(self) -> Embed:

        reqs_list = [f"- {r.text}" for r in self.requirements]
        reqs_list.extend(
            [f"- {r.text} - **(Global)**" for r in self.manager.global_requirements]
        )
        field_value = ("\n".join(reqs_list)) if reqs_list else "`Not Set`"
        linked_role = await self.role

        return U.make_embed(
            title=f"Position Status for: __{self.name}__",
            description=(
                "__**Description**__\n"
                f"{self.description if self.description else '`Not Set`'}\n"
                f"{U.draw_line(extra=25)}\n\n"
                
                "__**Role**__\n"
                f"{linked_role.mention if linked_role else '`Not Set`'}\n"
            ),
            fields=[
                EmbedField(
                    name="__Training Requirements__",
                    value=field_value,
                    inline=False
                )
            ]
        )

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        return PositionStatusView(user, self)

################################################################################
    async def set_name(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Position Name",
            attribute="Name",
            cur_val=self.name,
            example="eg. 'Bartender'"
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.name = modal.value

################################################################################
    async def set_description(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Position Description",
            attribute="Description",
            cur_val=self.description,
            example="eg. 'The bartender is responsible for serving drinks.'",
            max_length=500,
            multiline=True,
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.description = modal.value

################################################################################
    async def set_role(self, interaction: Interaction) -> None:

        guild = self.bot.get_guild(self.bot.SPB_ID)
        options = [SelectOption(label=role.name, value=str(role.id)) for role in guild.roles]
        prompt = U.make_embed(
            title="Set Role",
            description="Please select the role that should be linked to this position."
        )
        view = FroggeMultiMenuSelect(interaction.user, options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.role = guild.get_role(int(view.value))

################################################################################
    async def add_requirement(self, interaction: Interaction) -> None:

        if len(self._requirements) >= self.bot.MAX_SELECT_OPTIONS:
            error = MaxItemsReached("Position Requirement", self.bot.MAX_SELECT_OPTIONS)
            await error.send(interaction)
            return

        modal = BasicTextModal(
            title="Add Requirement",
            attribute="Requirement Text",
            example="eg. 'Must be able to mix drinks.'"
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        new_req = Requirement.new(self._mgr, self.id, modal.value)
        self._requirements.append(new_req)

################################################################################
    async def _select_requirement(self, interaction: Interaction) -> Optional[Requirement]:

        prompt = U.make_embed(
            title="Modify Requirement",
            description="Please select the requirement you would like to modify."
        )
        view = FroggeMultiMenuSelect(interaction.user, [req.select_option() for req in self._requirements])

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return None

        return next((r for r in self._requirements if r.id == int(view.value)))

################################################################################
    async def modify_requirement(self, interaction: Interaction) -> None:

        req = await self._select_requirement(interaction)
        if req is None:
            return

        modal = BasicTextModal(
            title="Modify Requirement",
            attribute="Requirement Text",
            cur_val=req.text
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        req.text = modal.value

################################################################################
    async def remove_requirement(self, interaction: Interaction) -> None:

        req = await self._select_requirement(interaction)
        if req is None:
            return

        await req.remove(interaction)

################################################################################
    def select_option(self, selected: bool = False) -> SelectOption:

        return SelectOption(
            label=self.name,
            value=str(self.id),
            default=selected
        )

################################################################################
