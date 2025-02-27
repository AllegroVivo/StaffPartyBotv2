from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Dict, Optional

from discord import Interaction, User, Embed, EmbedField, SelectOption

from Classes.Common import ObjectManager
from Errors import MaxItemsReached
from UI.Positions import PositionManagerMenuView
from .Position import Position
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import StaffPartyBot, Requirement
    from UI.Common import FroggeView, BasicTextModal, FroggeMultiMenuSelect
################################################################################

__all__ = ("PositionManager", )

################################################################################
class PositionManager(ObjectManager):

    __slots__ = (
        "_requirements",
    )
    
################################################################################
    def __init__(self, state: StaffPartyBot) -> None:

        super().__init__(state)

        self._requirements: List[Requirement] = []
    
################################################################################
    async def load_all(self, payload: Dict[str, Any]) -> None:
        
        self._managed = [Position(self, **pos) for pos in payload["positions"]]
        self._requirements = [Requirement(self, **req) for req in payload["global_requirements"]]

################################################################################
    async def finalize_load(self) -> None:

        for req in self._requirements:
            req.finalize_load()

################################################################################
    @property
    def global_requirements(self) -> List[Requirement]:

        return self._requirements

################################################################################
    @property
    def positions(self) -> List[Position]:

        self._managed.sort(key=lambda p: p.name)
        return self._managed

################################################################################
    def select_options(self) -> List[SelectOption]:

        return [p.select_option() for p in self.positions]

################################################################################
    async def status(self) -> Embed:

        pos_name_list = U.list_to_columns([p.name for p in self.positions], 2)
        return U.make_embed(
            title="Positions Management",
            fields=[
                EmbedField(
                    name="__Registered Positions__",
                    value=pos_name_list[0],
                    inline=True
                ),
                EmbedField(
                    name="** **",
                    value=pos_name_list[1],
                    inline=True
                ),
                EmbedField(
                    name="__Global Requirements__",
                    value="\n".join([f"- {req.text}" for req in self.global_requirements]),
                    inline=False
                )
            ]
        )

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:
        
        return PositionManagerMenuView(user, self)

################################################################################
    def get_position(self, name: str) -> Optional[Position]:

        return next((p for p in self.positions if p.name.lower() == name.lower()), None)

################################################################################
    async def add_item(self, interaction: Interaction) -> None:

        # This needs to be MAX_SELECT_OPTIONS because we use a multiselect menu
        # in some places, and we can only use a single selector for a multiselect.
        if len(self._managed) >= self.bot.MAX_SELECT_OPTIONS:
            error = MaxItemsReached("Positions", self.bot.MAX_SELECT_OPTIONS)
            await interaction.respond(embed=error, ephemeral=True)
            return

        modal = BasicTextModal(
            title="Add Position",
            attribute="Position Name",
            example="eg. 'Bartender'"
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        pos_name = modal.value
        existing = self.get_position(pos_name)
        if existing is not None:
            error = U.make_error(
                title="Position Exists",
                message=f"The position `{pos_name}` already exists.",
                solution=f"Try a different name for the position."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        position = Position.new(self, pos_name)
        self._managed.append(position)

        await position.menu(interaction)

################################################################################
    async def select_position(self, interaction: Interaction) -> Optional[Position]:

        prompt = U.make_embed(
            title="Select Position",
            description="Please select a position from the picker below."
        )
        view = FroggeMultiMenuSelect(interaction.user, [p.select_option() for p in self.positions])

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return None

        return self[view.value]

################################################################################
    async def modify_item(self, interaction: Interaction) -> None:
        
        pos = await self.select_position(interaction)
        if pos is None:
            return

        await pos.menu(interaction)

################################################################################
    async def remove_item(self, interaction: Interaction) -> None:

        pos = await self.select_position(interaction)
        if pos is None:
            return

        await pos.remove(interaction)
    
################################################################################
    async def add_requirement(self, interaction: Interaction) -> None:

        if len(self._requirements) >= self.bot.MAX_MULTI_SELECT_OPTIONS:
            error = MaxItemsReached("Global Requirements", self.bot.MAX_MULTI_SELECT_OPTIONS)
            await interaction.respond(embed=error, ephemeral=True)
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

        new_req = Requirement.new(self, None, modal.value)
        self._requirements.append(new_req)

################################################################################
    def get_global_requirement(self, req_id: int) -> Optional[Requirement]:

        return next((req for req in self.global_requirements if req.id == int(req_id)), None)

################################################################################
    async def _select_requirement(self, interaction: Interaction) -> Optional[Requirement]:

        prompt = U.make_embed(
            title="Select Requirement",
            description="Please select a global requirement from the picker below."
        )
        view = FroggeMultiMenuSelect(interaction.user, [req.select_option() for req in self.global_requirements])

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return None

        return self.get_global_requirement(view.value)

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
