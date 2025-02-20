from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar, Any, Dict

from Classes.Common import Identifiable
from Enums import Weekday

if TYPE_CHECKING:
    from Classes import Venue, StaffPartyBot
################################################################################

__all__ = ("VenueHours", )

VH = TypeVar("VH", bound="VenueHours")

################################################################################
class VenueHours(Identifiable):

    __slots__ = (
        "_parent",
        "_day",
        "_open_hour",
        "_open_minute",
        "_close_hour",
        "_close_minute",
        "_interval_type",
        "_interval_arg",
    )

################################################################################
    def __init__(self, parent: Venue, id: int, **kwargs) -> None:

        # This parameter needs to remain as 'id' without the leading underscore
        # since we're just dropping in the kwargs from the database query.
        super().__init__(id)

        self._parent: Venue = parent
        self._day: Weekday = kwargs.pop("day")

        self._open_hour: int = kwargs.pop("open_hour")
        self._open_minute: int = kwargs.pop("open_minute")
        self._close_hour: int = kwargs.pop("close_hour")
        self._close_minute: int = kwargs.pop("close_minute")
        self._interval_type: int = kwargs.pop("interval_type")
        self._interval_arg: int = kwargs.pop("interval_arg")

################################################################################
    @classmethod
    def from_xiv_schedule(cls: Type[VH], parent: Venue, data: Dict[str, Any]) -> VH:

        new_data = parent.bot.db.insert.venue_schedule()

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._parent.bot

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.venue_hours(self.id)

################################################################################
