from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List, Dict, Any

from discord import User, Embed, Role

from Classes.Common import ManagedObject, LazyRole

if TYPE_CHECKING:
    from Classes import PositionManager, Requirement
    from UI.Common import FroggeView
################################################################################

__all__ = ("Position", )

################################################################################
class Position(ManagedObject):

    __slots__ = (
        "_name",
        "_requirements",
        "_role",
        "_description",
    )

################################################################################
    def __init__(self, mgr: PositionManager, _id: int, **kwargs) -> None:

        super().__init__(mgr, _id)

        self._name: Optional[str] = kwargs.get("name")
        self._requirements: List[Requirement] = kwargs.get("requirements", [])
        self._role: LazyRole = LazyRole(self, kwargs.get("role_id"))
        self._description: Optional[str] = kwargs.get("description")

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

        pass

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        pass

################################################################################
