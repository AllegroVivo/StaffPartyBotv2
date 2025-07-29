from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ApplicationContext, Cog, SlashCommandGroup, InteractionContextType

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################
class Venues(Cog):

    def __init__(self, bot: StaffPartyBot):

        self.bot: StaffPartyBot = bot

################################################################################

    venues = SlashCommandGroup(
        name="venue",
        description="Commands for venue- and internship-related tasks and queries.",
    )

################################################################################
    @venues.command(
        name="profile",
        description="View and edit your venue's internship profile & status.",
    )
    async def venue_profile(self, ctx: ApplicationContext) -> None:

        if not await self.bot.is_loaded(ctx.interaction):
            return

        await self.bot.venue_manager.new_venue_menu(ctx.interaction)

################################################################################
def setup(bot: StaffPartyBot) -> None:

    bot.add_cog(Venues(bot))

################################################################################
