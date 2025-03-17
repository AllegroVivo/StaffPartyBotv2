from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from discord import Interaction, User

from .BGCheck import BGCheck

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("BGCheckManager", )

################################################################################
class BGCheckManager:

    __slots__ = (
        "_state",
        "_bg_checks",
    )

################################################################################
    def __init__(self, state: StaffPartyBot) -> None:

        self._state: StaffPartyBot = state
        self._bg_checks: List[BGCheck] = []

################################################################################
    async def load_all(self, payload: Dict[str, Any]) -> None:

        self._bg_checks = [BGCheck(self, **data) for data in payload["bg_checks"]]

################################################################################
    def __getitem__(self, user_id: int) -> Optional[BGCheck]:

        return next((bg for bg in self._bg_checks if bg.user_id == int(user_id)), None)

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._state

################################################################################
    async def start_bg_check(self, interaction: Interaction) -> None:

        bg_check = self[interaction.user.id]
        if bg_check is None:
            bg_check = BGCheck.new(self, interaction.user)
            self._bg_checks.append(bg_check)

        await bg_check.menu(interaction)

################################################################################
    async def staff_experience(self, interaction: Interaction, user: User) -> None:

        bg_check = self[user.id]
        if bg_check is None:
            bg_check = BGCheck.new(self, user)
            self._bg_checks.append(bg_check)

        await bg_check.staff_experience(interaction)

################################################################################
