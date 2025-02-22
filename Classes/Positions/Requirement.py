from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import User, Embed

from Classes.Common import Identifiable

if TYPE_CHECKING:
    from Classes import PositionManager, Position
    from UI.Common import FroggeView
################################################################################

__all__ = ("Requirement", )

################################################################################
class Requirement(Identifiable):

    __slots__ = (
        "_mgr",
        "_position",
        "_text",
    )

################################################################################
    def __init__(self, mgr: PositionManager, _id: int, **kwargs) -> None:

        super().__init__(_id)
        self._mgr: PositionManager = mgr

        self._position: Optional[Position] = kwargs.get("position", kwargs.get("position_id"))
        self._text: Optional[str] = kwargs.get("text")

################################################################################
    def finalize_load(self) -> None:

        if self._position and isinstance(self._position, int):
            self._position = self._mgr[self._position]

################################################################################
    async def status(self) -> Embed:

        pass

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        pass

################################################################################
