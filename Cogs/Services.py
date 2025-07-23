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
class Services(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################

    services = SlashCommandGroup(
        name="services",
        description="Commands for service related tasks and queries.",
        contexts=[InteractionContextType.guild]
    )

################################################################################
    @services.command(
        name="menu",
        description="Open the service request menu.",
    )
    async def service_menu(self, ctx: ApplicationContext) -> None:

        await self.bot.services_manager.user_menu(ctx.interaction)

################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Services(bot))

################################################################################
