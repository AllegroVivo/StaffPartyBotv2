from __future__ import annotations

from typing import TYPE_CHECKING, List, Type, TypeVar

from discord import SelectOption, Interaction

from Enums import DataCenter, GameWorld
from UI.Common import ConfirmCancelView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import BGCheck, StaffPartyBot
################################################################################

__all__ = ("BGCheckVenue", )

V = TypeVar("V", bound="BGCheckVenue")

################################################################################
class BGCheckVenue:

    def __init__(self, **kwargs):

        self.id: int = kwargs.pop("id")
        self.name: str = kwargs.pop("name")
        self.data_center: DataCenter = DataCenter(kwargs.pop("data_center"))
        self.world: GameWorld = GameWorld(kwargs.pop("world"))
        self.jobs: List[str] = kwargs.pop("jobs")

################################################################################
    @classmethod
    def new(
        cls: Type[V],
        parent: BGCheck,
        name: str,
        data_center: DataCenter,
        world: GameWorld,
        jobs: List[str]
    ) -> V:

        new_data = parent.bot.db.insert.bg_check_venue(
            parent.id, name, data_center.value, world.value, jobs
        )
        return cls(new_data["id"], name, data_center, world, jobs)

################################################################################
    def __eq__(self, other: BGCheckVenue) -> bool:

        return self.id == other.id

################################################################################
    def delete(self, bot: StaffPartyBot) -> None:

        bot.db.delete.bg_check_venue(self.id)

################################################################################
    def format(self) -> str:

        return (
            f"**{self.name}:** {self.world.proper_name} "
            f"({self.data_center.proper_name})\n"
            f"Jobs: {', '.join(self.jobs)}"
        )

################################################################################
    def select_option(self) -> SelectOption:

        return SelectOption(
            label=self.name,
            value=self.name,
            description=U.string_clamp(f"{self.world.proper_name} ({self.data_center.proper_name})", 100),
        )

################################################################################
    async def remove(self, interaction: Interaction) -> bool:

        prompt = U.make_embed(
            title="Remove BG Check Venue",
            description=(
                f"Are you sure you want to remove **{self.name}** from your "
                f"background check?"
            )
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return False

        self.delete(interaction.client)  # type: ignore
        return True

################################################################################
