from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Dict, Any

from discord import Interaction, SelectOption

from Classes.Common import Identifiable
from Utilities import Utilities as U
from UI.Common import ConfirmCancelView

if TYPE_CHECKING:
    from Classes import PositionManager, Position, StaffPartyBot
################################################################################

__all__ = ("Requirement", )

R = TypeVar("R", bound="Requirement")

################################################################################
class Requirement(Identifiable):

    __slots__ = (
        "_mgr",
        "_position",
        "_text",
    )

################################################################################
    def __init__(self, mgr: PositionManager, id: int, **kwargs) -> None:

        super().__init__(id)
        self._mgr: PositionManager = mgr

        self._position: Optional[Position] = kwargs.get("position", kwargs.get("position_id"))
        self._text: str = kwargs.get("text")

################################################################################
    @classmethod
    def new(cls: Type[R], mgr: PositionManager, pos_id: Optional[int], text: str) -> R:

        new_data = mgr.bot.db.insert.requirement(pos_id, text)
        pos = mgr[pos_id] if pos_id else None
        return cls(mgr, new_data["id"], text=text, position=pos)

################################################################################
    def finalize_load(self) -> None:

        if self._position and isinstance(self._position, int):
            self._position = self._mgr[self._position]

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._mgr.bot

################################################################################
    @property
    def position(self) -> Optional[Position]:

        return self._position

################################################################################
    @property
    def text(self) -> str:

        return self._text

    @text.setter
    def text(self, value: str) -> None:

        self._text = value
        self.update()

################################################################################
    def update(self) -> None:

        self.bot.db.update.requirement(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "text": self._text,
        }

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.requirement(self.id)

        if self._position is not None:
            self._position._requirements.remove(self)
        else:
            self._mgr._requirements.remove(self)

################################################################################
    def select_option(self) -> SelectOption:

        return SelectOption(label=self.text, value=str(self.id))

################################################################################
    async def remove(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title=f"Remove ",
            description=f"Are you sure you want to remove this requirement?"
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.delete()

################################################################################
