from __future__ import annotations

from datetime import time, date, datetime, timedelta
from typing import TYPE_CHECKING, List, Type, TypeVar, Dict
from zoneinfo import ZoneInfo

from Classes.Common import Identifiable
from Enums import Weekday
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import StaffPartyBot, DJProfile
################################################################################

__all_ = ("DJAvailability",)

A = TypeVar("A", bound="DJAvailability")

################################################################################
class DJAvailability(Identifiable):

    __slots__ = (
        "_parent",
        "_weekday",
        "_start_min_local",
        "_end_min_local",
    )

################################################################################
    def __init__(self, parent: DJProfile, id: int, **kwargs) -> None:

        super().__init__(id)

        self._parent: DJProfile = parent

        self._weekday: Weekday = Weekday(kwargs.pop("weekday"))
        self._start_min_local: int = kwargs.pop("start_min_local")
        self._end_min_local: int = kwargs.pop("end_min_local")

################################################################################
    @classmethod
    def new_range(
        cls: Type[A],
        parent: DJProfile,
        day: Weekday,
        start_min_local: int,
        end_min_local: int,
    ) -> A:

        new_data = parent.bot.db.insert.dj_availability(
            parent.id, day.value, start_min_local, end_min_local
        )
        return cls(parent=parent, **new_data)

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._parent.bot

################################################################################
    @property
    def timezone(self) -> ZoneInfo:

        return self._parent.timezone

################################################################################
    @property
    def weekday(self) -> Weekday:

        return self._weekday

################################################################################
    @property
    def start_min_local(self) -> int:

        return self._start_min_local

################################################################################
    @property
    def end_min_local(self) -> int:

        return self._end_min_local

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
    def _next_local_dt_for(self, minutes_local: int, weekday) -> datetime:
        # Get the next date for this weekday in the profile's timezone
        d = self.get_local_date_for_weekday(self.timezone, weekday.value)

        # If the range ends at 24:00 (i.e., 1440 minutes), roll to next day 00:00
        if minutes_local >= 1440:
            minutes_local -= 1440
            d += timedelta(days=1)

        h, m = divmod(minutes_local, 60)
        try:
            ret = datetime(d.year, d.month, d.day, h, m, tzinfo=self.timezone)
        except ValueError:
            print(f"Invalid time {h}:{m} on date {d} in timezone {self.timezone}")
            raise
        return ret

################################################################################
    @property
    def start_timestamp(self) -> str:

        dt_local = self._next_local_dt_for(self.start_min_local, self.weekday)
        return U.format_dt(dt_local.astimezone(ZoneInfo("UTC")), "t")

################################################################################
    @property
    def end_timestamp(self) -> str:

        dt_local = self._next_local_dt_for(self.end_min_local, self.weekday)
        return U.format_dt(dt_local.astimezone(ZoneInfo("UTC")), "t")

################################################################################
    @staticmethod
    def long_availability_status(avails: List[DJAvailability]) -> str:

        if not avails:
            return "`No Availability Set`"

        by_day: Dict[Weekday, List[DJAvailability]] = {}
        for a in avails:
            by_day.setdefault(a.weekday, []).append(a)

        lines = ["*(Times are displayed in\nyour local time zone.)*\n"]
        for wd in Weekday:
            day_ranges = sorted(by_day.get(wd, []), key=lambda x: x.start_min_local)
            if not day_ranges:
                lines.append(f"{wd.proper_name}: `Not Available`")
            else:
                segs = [f"{r.start_timestamp} - {r.end_timestamp}" for r in day_ranges]
                lines.append(f"{wd.proper_name}: " + "  |  ".join(segs))

        return "\n".join(lines)

################################################################################
    @staticmethod
    def short_availability_status(availability: List[DJAvailability]) -> str:

        availability.sort(key=lambda x: x.weekday.value)
        return "\n".join([
            (
                f"{a.weekday.proper_name}: "
                f"{a.start_timestamp} - {a.end_timestamp}"
            ) for a in availability
        ]) if availability else "`No Availability Set`"

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.dj_profile_availability(self.id)

################################################################################
