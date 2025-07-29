from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType,
    InteractionContextType
)

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################
class DJOperations(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################

    djs = SlashCommandGroup(
        name="dj",
        description="Commands for DJ-related tasks and queries.",
    )

################################################################################
    @djs.command(
        name="profile",
        description="View and edit your training registration profile & status."
    )
    async def staff_profile(self, ctx: ApplicationContext) -> None:

        if not self.bot.is_loaded(ctx.interaction):
            return

        await self.bot.dj_profile_manager.user_menu(ctx.interaction)

################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(DJOperations(bot))

################################################################################
