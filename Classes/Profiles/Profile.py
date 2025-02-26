from __future__ import annotations

from typing import TYPE_CHECKING

from discord import User, Embed

from Classes.Common import ManagedObject, LazyUser

if TYPE_CHECKING:
    from Classes import ProfileManager
    from UI.Common import FroggeView
################################################################################

__all__ = ("Profile", )

################################################################################
class Profile(ManagedObject):

    __slots__ = (
        "_user",
        "_details",
        "_aag",
        "_personality",
        "_images",
        "_post_msg",
    )

################################################################################
    def __init__(self, mgr: ProfileManager, id: int, **kwargs) -> None:

        super().__init__(mgr, id)

        self._user: LazyUser = LazyUser(self, kwargs["user_id"])

################################################################################
    @property
    async def user(self) -> User:

        return await self._user.get()

    @property
    def user_id(self) -> int:

        return self._user.id

################################################################################
    async def status(self) -> Embed:

        pass

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        pass

################################################################################
