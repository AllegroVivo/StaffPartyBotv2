from __future__ import annotations

from datetime import time, date, datetime, timedelta
from typing import TYPE_CHECKING, List, Type, TypeVar
from zoneinfo import ZoneInfo

from Classes.Profiles.Availability import Availability
from Enums import Weekday
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import StaffPartyBot, DJProfile
################################################################################

__all_ = ("DJAvailability",)

A = TypeVar("A", bound="DJAvailability")

################################################################################
class DJAvailability(Availability):

    __slots__ = (
        "_parent",
        "_day",
        "_start_hour",
        "_start_minute",
        "_end_hour",
        "_end_minute"
    )

################################################################################
    def __init__(self, parent: DJProfile, id: int, **kwargs) -> None:

        super().__init__(None, id, **kwargs)  # type: ignore

        self._parent: DJProfile = parent

################################################################################
    @classmethod
    def new(
        cls: Type[A],
        parent: DJProfile,
        day: Weekday,
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int
    ) -> A:

        new_data = parent.bot.db.insert.dj_availability(
            parent.id, day.value, start_hour, start_minute, end_hour, end_minute
        )
        return cls(parent=parent, **new_data)

################################################################################
    @property
    def timezone(self) -> ZoneInfo:

        return self._parent.timezone

################################################################################
    @property
    def start_timestamp(self) -> str:

        next_date = self.get_local_date_for_weekday(self.timezone, self.day.value)
        dt = datetime(
            year=next_date.year,
            month=next_date.month,
            day=next_date.day,
            hour=self.start_time.hour,
            minute=self.start_time.minute,
            tzinfo=ZoneInfo("UTC")
        )
        return U.format_dt(dt.replace(tzinfo=ZoneInfo("UTC")), "t")

################################################################################
    @property
    def end_timestamp(self) -> str:

        next_date = self.get_local_date_for_weekday(self.timezone, self.day.value)
        dt = datetime(
            year=next_date.year,
            month=next_date.month,
            day=next_date.day,
            hour=self.end_time.hour,
            minute=self.end_time.minute,
            tzinfo=ZoneInfo("UTC")
        )
        return U.format_dt(dt.replace(tzinfo=ZoneInfo("UTC")), "t")

################################################################################
    @staticmethod
    def long_availability_status(availability: List[DJAvailability]) -> str:

        if not availability:
            return "`No Availability Set`"

        ret = ""

        availability.sort(key=lambda x: x.day.value)
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
    def short_availability_status(availability: List[DJAvailability]) -> str:

        availability.sort(key=lambda x: x.day.value)
        return "\n".join([
            (
                f"{a.day.proper_name}: "
                f"{a.start_timestamp} - {a.end_timestamp}"
            ) for a in availability
        ]) if availability else "`No Availability Set`"

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.dj_profile_availability(self.id)

################################################################################
