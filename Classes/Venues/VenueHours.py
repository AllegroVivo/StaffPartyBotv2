from __future__ import annotations
import random
import calendar
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Type, TypeVar, Any, Dict, Optional

from Classes.Common import Identifiable
from Enums import Weekday, XIVIntervalType
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import Venue, StaffPartyBot, XIVScheduleComponent
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

        day = kwargs.get("day")
        interval_type = kwargs.get("interval_type")
        self._day: Weekday = Weekday(day) if day is not None else None
        self._open_hour: int = kwargs.get("start_hour")
        self._open_minute: int = kwargs.get("start_minute")
        self._close_hour: Optional[int] = kwargs.get("end_hour")
        self._close_minute: Optional[int] = kwargs.get("end_minute")
        self._interval_type: XIVIntervalType = (
            XIVIntervalType(interval_type)
            if interval_type is not None
            else None
        )
        self._interval_arg: int = kwargs.get("interval_arg")

################################################################################
    @classmethod
    def from_xiv_schedule(cls: Type[VH], parent: Venue, xiv: XIVScheduleComponent) -> VH:

        new_data = parent.bot.db.insert.venue_schedule(parent.id)
        self: VH = cls(parent, new_data["id"])
        self.update_from_xiv_venue(xiv)
        return self

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._parent.bot

################################################################################
    def open_ts(self) -> str:

        res = self.resolve()
        return U.format_dt(res, "t")

################################################################################
    def close_ts(self) -> str:

        if self._close_hour is None or self._close_minute is None:
            return "N/A"

        dt = self.resolve()
        if self._open_hour > self._close_hour:
            dt += timedelta(days=1)

        return U.format_dt(dt, "t")

################################################################################
    def update(self) -> None:

        self.bot.db.update.venue_hours(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "day": self._day.value,
            "start_hour": self._open_hour,
            "start_minute": self._open_minute,
            "end_hour": self._close_hour,
            "end_minute": self._close_minute,
            "interval_type": self._interval_type.value,
            "interval_arg": self._interval_arg,
        }

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.venue_hours(self.id)

################################################################################
    def update_from_xiv_venue(self, xiv: XIVScheduleComponent) -> None:

        self._day = Weekday(xiv.day) if xiv.day is not None else None
        self._open_hour = xiv.utc.start.hour
        self._open_minute = xiv.utc.start.minute
        self._close_hour = xiv.utc.end.hour if xiv.utc.end is not None else None
        self._close_minute = xiv.utc.end.minute if xiv.utc.end is not None else None
        self._interval_type = XIVIntervalType(xiv.interval.interval_type)
        self._interval_arg = xiv.interval.arg

        self.update()

################################################################################
    def resolve(self) -> datetime:
        """Determines the next scheduled opening date and time."""

        today = datetime.today()
        next_open_date = None

        # If interval type is Every X Weeks
        if self._interval_type == XIVIntervalType.EveryXWeeks:
            next_open_date = self._calculate_next_weekly_schedule(today)

        # If interval type is Every Xth Day of the Month
        elif self._interval_type == XIVIntervalType.EveryXthDayOfTheMonth:
            next_open_date = self._calculate_next_monthly_schedule(today)

        if next_open_date:
            return next_open_date.replace(hour=self._open_hour, minute=self._open_minute)

        return datetime.min

################################################################################
    def _calculate_next_weekly_schedule(self, today: datetime) -> datetime:
        """Finds the next occurrence of the scheduled weekday, then applies the interval."""

        # Get the next occurrence of self._day
        days_until_next = (self._day.value - today.weekday()) % 7
        first_occurrence = today + timedelta(days=days_until_next)

        # Apply the interval (every X weeks)
        return first_occurrence + timedelta(weeks=self._interval_arg)

################################################################################
    def _calculate_next_monthly_schedule(self, today: datetime) -> datetime:
        """Finds the Xth (or Xth-last) occurrence of the scheduled weekday in the current or next month."""

        year, month = today.year, today.month

        # Find all occurrences of the given weekday in this month
        weekday_occurrences = [
            datetime(year, month, day)
            for day in range(1, calendar.monthrange(year, month)[1] + 1)
            if datetime(year, month, day).weekday() == self._day.value
        ]

        # Select the correct occurrence
        if self._interval_arg > 0:
            if len(weekday_occurrences) >= self._interval_arg:
                return weekday_occurrences[self._interval_arg - 1]
        elif self._interval_arg < 0:
            if len(weekday_occurrences) >= abs(self._interval_arg):
                return weekday_occurrences[self._interval_arg]

        # If the specified occurrence doesn't exist in this month, move to next month
        next_month = today.replace(day=28) + timedelta(days=4)  # Moves to the next month
        next_month = next_month.replace(day=1)  # Set to first day of next month
        return self._calculate_next_monthly_schedule(next_month)

################################################################################
    def format(self) -> str:
        """
        Returns a human-readable schedule string, taking into account the interval type
        (e.g. Every X weeks vs. the Xth or Xth-last weekday of the month) and the open/close times.
        """

        day_name = self._day.proper_name if self._day else "Unknown Day"

        # Convert the open/close times to strings
        open_str = self.open_ts()
        close_str = self.close_ts()

        if not self._interval_type:
            # Fallback if interval type is not set
            return f"{day_name}: {open_str} - {close_str}"

        if self._interval_type == XIVIntervalType.EveryXWeeks:
            # e.g. "Every 2 weeks on Tuesday: 10:00 AM - 2:00 PM"
            return (
                f"Every {self._interval_arg} week(s) on {day_name}: "
                f"{open_str} - {close_str}"
            )

        elif self._interval_type == XIVIntervalType.EveryXthDayOfTheMonth:
            # e.g. "2nd Tuesday of the month: 10:00 AM - 2:00 PM"
            ordinal_str = self._get_ordinal_string(self._interval_arg)
            return (
                f"{ordinal_str} {day_name} of the month: "
                f"{open_str} - {close_str}"
            )

        # Add more elif blocks if you have other interval types...
        else:
            # Fallback for unknown/unsupported interval types
            return f"{day_name}: {open_str} - {close_str}"

################################################################################
    def _get_ordinal_string(self, n: int) -> str:
        """
        Convert an integer into a string describing its ordinal position.
        Examples:
          1 -> '1st'
          2 -> '2nd'
          3 -> '3rd'
          4 -> '4th'
          -1 -> 'last'
          -2 -> '2nd-last'
          -3 -> '3rd-last'
        """

        # Handle negative values as "nth-last"
        if n < 0:
            abs_n = abs(n)
            suffix = self._positive_ordinal_suffix(abs_n)
            # e.g. abs_n=2 -> "2nd-last"
            return f"{suffix}-last"
        else:
            # e.g. n=2 -> "2nd"
            return self._positive_ordinal_suffix(n)

################################################################################
    @staticmethod
    def _positive_ordinal_suffix(n: int) -> str:
        """
        Returns the English ordinal suffix for a positive integer.
        1 -> '1st', 2 -> '2nd', 3 -> '3rd', 4 -> '4th', etc.
        """

        # Special cases: 11th, 12th, 13th
        if 11 <= (n % 100) <= 13:
            return f"{n}th"

        # Cases for 1, 2, 3
        last_digit = n % 10
        if last_digit == 1:
            return f"{n}st"
        elif last_digit == 2:
            return f"{n}nd"
        elif last_digit == 3:
            return f"{n}rd"
        else:
            return f"{n}th"

################################################################################
