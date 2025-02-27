from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, Optional, List

from .ProfileSection import ProfileSection
from Enums import Gender, Pronoun, Race, Clan, Orientation, DataCenter, GameWorld

if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all__ = ("ProfileAtAGlance", )

################################################################################
class ProfileAtAGlance(ProfileSection):

    __slots__ = (
        "_gender",
        "_pronouns",
        "_race",
        "_clan",
        "_orientation",
        "_height",
        "_age",
        "_mare",
        "_data_centers",
    )

################################################################################
    def __init__(self, parent: Profile, **kwargs) -> None:

        super().__init__(parent)

        self._pronouns: List[Pronoun] = [Pronoun(p) for p in kwargs.get("pronouns", [])]

        gender: str = kwargs.get("gender")
        race = kwargs.get("race")
        clan = kwargs.get("clan")
        orientation = kwargs.get("orientation")
        data_centers = kwargs.get("data_centers", [])

        self._gender: Optional[Gender] = (
            Gender(int(gender))
            if gender is not None and gender.isdigit()
            else gender
        )
        self._race: Optional[Race] = (
            Race(int(race))
            if race is not None and race.isdigit()
            else race
        )
        self._clan: Optional[Clan] = (
            Clan(int(clan))
            if clan is not None and clan.isdigit()
            else clan
        )
        self._orientation: Optional[Orientation] = (
            Orientation(int(orientation))
            if orientation is not None and orientation.isdigit()
            else orientation
        )
        self._height: Optional[int] = kwargs.get("height")
        self._age: Optional[str] = kwargs.get("age")
        self._mare: Optional[str] = kwargs.get("mare")
        self._data_centers: List[DataCenter] = [DataCenter(dc) for dc in data_centers]

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "pronouns": [p.value for p in self._pronouns],
            "gender": (
                str(self._gender.value)
                if isinstance(self._gender, Gender)
                else self._gender
            ),
            "race": (
                str(self._race.value)
                if isinstance(self._race, Race)
                else self._race
            ),
            "clan": (
                str(self._clan.value)
                if isinstance(self._clan, Clan)
                else self._clan
            ),
            "orientation": (
                str(self._orientation.value)
                if isinstance(self._orientation, Orientation)
                else self._orientation
            ),
            "height": self._height,
            "age": self._age,
            "mare": self._mare,
            "data_center": [dc.value for dc in self._data_centers],
        }

################################################################################
