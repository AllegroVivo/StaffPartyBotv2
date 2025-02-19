from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from discord import Interaction, Embed, User, SelectOption

from .FroggeObject import FroggeObject
from logger import log
from UI.Common import ConfirmCancelView
from Utilities import Utilities as U
from .Identifiable import Identifiable

if TYPE_CHECKING:
    from Classes import ObjectManager, RentARaBot, GuildData
    from UI.Common import FroggeView
################################################################################

__all__ = ("ManagedObject",)

################################################################################
class ManagedObject(Identifiable, FroggeObject):

    __slots__ = (
        "_mgr",
    )

################################################################################
    def __init__(self, mgr: ObjectManager, _id: int) -> None:

        super().__init__(_id)
        FroggeObject.__init__(self)

        self._mgr: ObjectManager = mgr

################################################################################
    @property
    def bot(self) -> RentARaBot:

        return self._mgr.bot

################################################################################
    @property
    def manager(self) -> ObjectManager:

        return self._mgr

################################################################################
    @abstractmethod
    async def status(self) -> Embed:

        raise NotImplementedError

################################################################################
    @abstractmethod
    def get_menu_view(self, user: User) -> FroggeView:

        raise NotImplementedError

################################################################################
    def select_option(self) -> SelectOption:

        raise NotImplementedError

################################################################################
    async def menu(self, interaction: Interaction) -> None:

        embed = await self.status()
        view = self.get_menu_view(interaction.user)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

        if getattr(self, "update_post_components", None) is not None:
            await self.update_post_components()  # type: ignore

################################################################################
    async def remove(self, interaction: Interaction) -> None:

        type_name = self.__class__.__name__
        log.info(f"Removing {type_name}.")

        prompt = U.make_embed(
            title=f"Remove ",
            description=(
                f"Are you sure you want to remove this {type_name}?"
            )
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug(f"{type_name} removal cancelled.")
            return

        self.delete()

        log.info(f"{type_name} removed.")

################################################################################
