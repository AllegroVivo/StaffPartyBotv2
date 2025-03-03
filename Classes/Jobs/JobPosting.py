from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional, List, Type, TypeVar

from discord import User, Embed

from Classes.Common import ManagedObject, LazyUser, LazyMessage
from Enums import JobPostingType

if TYPE_CHECKING:
    from Classes import JobPostingManager, Position, Venue
    from UI.Common import FroggeView
################################################################################

__all__ = ("JobPosting", )

JP = TypeVar("JP", bound="JobPosting")

################################################################################
class JobPosting(ManagedObject):

    __slots__ = (
        "_venue",
        "_user",
        "_type",
        "_position",
        "_salary",
        "_start",
        "_end",
        "_description",
        "_post_msg",
        "_candidate",
        "_rejections",
        "_schedule_updated",
    )

################################################################################
    def __init__(self, mgr: JobPostingManager, id: int, **kwargs) -> None:

        super().__init__(mgr, id)

        self._venue: Venue = kwargs.get("venue", kwargs.pop("venue_id"))
        self._user: LazyUser = LazyUser(self, kwargs.get("user_id"))
        self._candidate: LazyUser = LazyUser(self, kwargs.get("candidate_id"))
        self._rejections: List[LazyUser] = [LazyUser(self, r) for r in kwargs.get("rejection_ids", [])]

        self._description: Optional[str] = kwargs.get("description")
        self._type: Optional[JobPostingType] = JobPostingType.Temporary
        self._position: Optional[Position] = kwargs.get("position", kwargs.pop("position_id"))
        self._post_msg: LazyMessage = LazyMessage(self, kwargs.get("post_url"))

        self._salary: Optional[str] = kwargs.get("salary")
        self._start: Optional[datetime] = kwargs.get("start_dt")
        self._end: Optional[datetime] = kwargs.get("end_dt")

        self._schedule_updated: bool = False

################################################################################
    def finalize_load(self) -> None:

        if isinstance(self._venue, int):
            self._venue = self.bot.venue_manager[self._venue]

        if self._position is not None and isinstance(self._position, int):
            self._position = self.bot.position_manager[self._position]

################################################################################
    @classmethod
    def new(cls: Type[JP], mgr: JobPostingManager, venue: Venue, user: User) -> JP:


################################################################################
    async def status(self) -> Embed:

        pass

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        pass

################################################################################
