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
class Staff(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################

    staff = SlashCommandGroup(
        name="staff",
        description="Commands for trainee-related tasks and queries.",
    )

################################################################################
    @staff.command(
        name="profile",
        description="View and edit your training registration profile & status."
    )
    async def staff_profile(self, ctx: ApplicationContext) -> None:

        if not await self.bot.is_loaded(ctx.interaction):
            return

        await self.bot.profile_manager.user_menu(ctx.interaction)

################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Staff(bot))

################################################################################
