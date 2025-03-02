from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING, List, Type, TypeVar, Union

from Classes.Common import Identifiable
from Enums import Weekday
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import Profile, TUser, StaffPartyBot
################################################################################

__all_ = ("Availability",)

A = TypeVar("A", bound="Availability")

################################################################################
class Availability(Identifiable):

    __slots__ = (
        "_parent",
        "_day",
        "_start_hour",
        "_start_minute",
        "_end_hour",
        "_end_minute"
    )

################################################################################
    def __init__(self, parent: Profile, id: int, **kwargs) -> None:

        super().__init__(id)

        self._parent: Profile = parent

        self._day: Weekday = (
            Weekday(kwargs.get("day"))
            if isinstance(kwargs.get("day"), int)
            else kwargs.get("day")
        )
        self._start_hour: int = kwargs.get("start_hour")
        self._start_minute: int = kwargs.get("start_minute")
        self._end_hour: int = kwargs.get("end_hour")
        self._end_minute: int = kwargs.get("end_minute")

################################################################################
    @classmethod
    def new(
        cls: Type[A],
        parent: Profile,
        day: Weekday,
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int
    ) -> A:

        new_data = parent.bot.db.insert.availability(
            parent.id, day.value, start_hour, start_minute, end_hour, end_minute
        )
        return cls(parent=parent, **new_data)

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._parent.bot

################################################################################
    @property
    def day(self) -> Weekday:

        return self._day

################################################################################
    @property
    def start_time(self) -> time:

        return time(self._start_hour, self._start_minute)

################################################################################
    @property
    def end_time(self) -> time:

        return time(self._end_hour, self._end_minute)

################################################################################
    @property
    def start_timestamp(self) -> str:

        return U.format_dt(U.time_to_datetime(self.start_time), "t")

################################################################################
    @property
    def end_timestamp(self) -> str:

        return U.format_dt(U.time_to_datetime(self.end_time), "t")

################################################################################
    @staticmethod
    def long_availability_status(availability: List[Availability]) -> str:

        if not availability:
            return "`No Availability Set`"

        ret = ""

        for i in [w for w in Weekday]:
            if i.value not in [a.day.value for a in availability]:
                ret += f"{i.proper_name}: `Not Available`\n"
            else:
                a = next((a for a in availability if a.day == i))
                ret += (
                    f"{a.day.proper_name}: "
                    f"{a.start_timestamp} - {a.end_timestamp}\n"
                )

        return "*(Times are displayed in\nyour local time zone.)*\n\n" + ret

################################################################################
    @staticmethod
    def short_availability_status(availability: List[Availability]) -> str:

        return "\n".join([
            (
                f"{a.day.proper_name}: "
                f"{a.start_timestamp} - {a.end_timestamp}\n"
            ) for a in availability
        ]) if availability else "`No Availability Set`"

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.profile_availability(self)

################################################################################
    def contains(self, range_start: time, range_end: time) -> bool:

        return self.start_time <= range_start and self.end_time >= range_end

################################################################################
    