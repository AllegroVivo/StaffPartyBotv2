from __future__ import annotations

from zoneinfo import ZoneInfo
from datetime import time, date, datetime, timedelta
from typing import TYPE_CHECKING, List, Type, TypeVar, Union
from zoneinfo import ZoneInfo

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

        next_date = self.get_local_date_for_weekday(self._parent.details.timezone, self.day.value)
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

        next_date = self.get_local_date_for_weekday(self._parent.details.timezone, self.day.value)
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
    def long_availability_status(availability: List[Availability]) -> str:

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
    def short_availability_status(availability: List[Availability]) -> str:

        availability.sort(key=lambda x: x.day.value)
        return "\n".join([
            (
                f"{a.day.proper_name}: "
                f"{a.start_timestamp} - {a.end_timestamp}"
            ) for a in availability
        ]) if availability else "`No Availability Set`"

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.profile_availability(self.id)

################################################################################
    def contains(self, range_start: time, range_end: time) -> bool:
        """
        Returns True if [range_start, range_end] is fully contained within
        [self.start_time, self.end_time], accounting for crossing midnight.
        """
        # Convert self's start & end to minutes from midnight
        s = self.start_time.hour * 60 + self.start_time.minute
        e = self.end_time.hour * 60 + self.end_time.minute
        if e <= s:
            e += 24 * 60  # crosses midnight

        # Convert the range's start & end similarly
        rs = range_start.hour * 60 + range_start.minute
        re = range_end.hour * 60 + range_end.minute
        if re <= rs:
            re += 24 * 60  # crosses midnight

        return s <= rs and e >= re

################################################################################
    @staticmethod
    def get_local_date_for_weekday(user_tz: ZoneInfo, selected_weekday: int) -> date:
        """
        Returns the date of the next occurrence of `selected_weekday` (0=Monday ... 6=Sunday)
        in the user's local timezone, based on 'now' in that same timezone.
        """
        # Current local date/time
        now_local = datetime.now(user_tz)
        today_local = now_local.date()
        # Monday=0 ... Sunday=6 in Python's weekday(), but your Weekday enum might differ.
        # Let's assume your "weekday.value" is also 0=Monday..6=Sunday. If not, adjust accordingly.

        today_wkday = now_local.weekday()  # 0=Monday..6=Sunday
        # The difference from the current day to the target day
        day_diff = (selected_weekday - today_wkday) % 7

        # If day_diff=0, that means "today" is already the chosen weekday.
        # If you want the *next* occurrence (not the current day), and day_diff=0, you could add 7.
        # For this example, we'll allow the same day if times are in the future.
        # day_diff = 7 if day_diff == 0 else day_diff

        chosen_date = today_local + timedelta(days=day_diff)
        return chosen_date

################################################################################
