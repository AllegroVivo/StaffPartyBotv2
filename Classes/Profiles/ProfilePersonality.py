from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Dict, Any

from .ProfileSection import ProfileSection

if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all__ = ("ProfilePersonality", )

################################################################################
class ProfilePersonality(ProfileSection):

    __slots__ = (
        "_likes",
        "_dislikes",
        "_personality",
        "_aboutme",
    )

################################################################################
    def __init__(self, parent: Profile, **kwargs) -> None:

        super().__init__(parent)

        self._likes: List[str] = kwargs.get("likes", [])
        self._dislikes: List[str] = kwargs.get("dislikes", [])
        self._personality: Optional[str] = kwargs.get("personality")
        self._aboutme: Optional[str] = kwargs.get("about_me")

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "likes": self._likes,
            "dislikes": self._dislikes,
            "personality": self._personality,
            "about_me": self._aboutme
        }

################################################################################
