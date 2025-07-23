from __future__ import annotations

from datetime import datetime, timedelta
from typing import TypeVar
################################################################################

__all__ = ("RevisitTimer", )

T = TypeVar("T")

################################################################################
class RevisitTimer:

    __slots__ = (
        "_context",
        "_created",
        "_revisit",
    )

################################################################################
    def __init__(self, ctx: T, duration_sec: int) -> None:

        self._context: T = ctx

        self._created: datetime = datetime.now()
        self._revisit: datetime = datetime.now() + timedelta(seconds=duration_sec)

################################################################################
    @property
    def context(self) -> T:

        return self._context

################################################################################
    def is_expired(self) -> bool:

        return datetime.now() >= self._revisit

################################################################################
