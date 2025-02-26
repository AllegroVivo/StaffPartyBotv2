from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from .ProfileSection import ProfileSection
from Utilities import Utilities as U, FroggeColor

if TYPE_CHECKING:
    from Classes import Profile, Position
################################################################################

__all__ = ("ProfileDetails", )

################################################################################
class ProfileDetails(ProfileSection):

    __slots__ = (
        "_name",
        "_url",
        "_color",
        "_jobs",
        "_rates",
        "_positions",
        "_availability",
        "_dm_pref",
        "_tz",
    )

################################################################################
    def __init__(self, parent: Profile, **kwargs) -> None:

        super().__init__(parent)

        self._name: Optional[str] = kwargs.get("name")
        self._url: Optional[str] = kwargs.get("url")
        self._color: FroggeColor = kwargs.get("color")
        self._jobs: List[str] = kwargs.get("jobs", [])
        self._rates: Optional[str] = kwargs.get("rates")
        self._positions: List[Position] = kwargs.get("positions", [])
        self._availability: List[PAvailability] = kwargs.get("availability", [])
        self._dm_pref: bool = kwargs.get("dm_pref", False)

################################################################################
