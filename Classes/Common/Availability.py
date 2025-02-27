from __future__ import annotations

from abc import ABC, abstractmethod
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
class Availability(Identifiable, ABC):

    __slots__ = (
        "_parent",
        "_day",
        "_start_hour",
        "_start_minute",
        "_end_hour",
        "_end_minute"
    )

################################################################################
    def __init__(self, parent: Union[Profile, TUser], id: int, **kwargs) -> None:

        super().__init__(id)

        self._parent: Union[Profile, TUser] = parent

        self._day: Weekday = kwargs.get("day")
        self._start_hour: int = kwargs.get("start_hour")
        self._start_minute: int = kwargs.get("start_minute")
        self._end_hour: int = kwargs.get("end_hour")
        self._end_minute: int = kwargs.get("end_minute")

################################################################################
    @classmethod
    @abstractmethod
    def new(
        cls: Type[A],
        parent: Union[Profile, TUser],
        day: Weekday,
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int
    ) -> A:

        raise NotImplementedError

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._parent.bot

################################################################################
    @property
    def parent(self) -> Union[Profile, TUser]:

        return self._parent

################################################################################
    @property
    def user_id(self) -> int:
        
        return self._parent.user_id
    
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

        days_list = [a.day for a in availability]
        for member in Weekday:
            if member not in days_list:
                ret += f"{member.proper_name}: `Not Available`\n"
            else:
                a = next((a for a in availability if a.day == member))
                ret += (
                    f"{a.day.proper_name}: "
                    f"{a.start_timestamp} - {a.end_timestamp}\n"
                )

        return (
            "*(Times are displayed in\n"
            "your local time zone.)*\n\n"
            
            f"{ret}"
        )

################################################################################
    @staticmethod
    def short_availability_status(availability: List[Availability]) -> str:

        if not availability:
            return "`No Availability Set`"

        ret = ""
        for a in availability:
            ret += (
                f"{a.day.proper_name}: "
                f"{a.start_timestamp} - {a.end_timestamp}\n"
            )

        return ret

################################################################################
    @abstractmethod
    def delete(self) -> None:

        raise NotImplementedError

################################################################################
    def contains(self, range_start: time, range_end: time) -> bool:

        return self.start_time <= range_start and self.end_time >= range_end

################################################################################
    