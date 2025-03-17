from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType,
    InteractionContextType,
    slash_command
)

from Classes.Core.HelpMessage import HelpMessage

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################
class Global(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################
    @slash_command(
        name="help",
        description="Get help with using the bot.",
        contexts=[InteractionContextType.guild]
    )
    async def help_menu(self, ctx: ApplicationContext) -> None:

        await HelpMessage(self.bot).menu(ctx.interaction)

################################################################################
    @slash_command(
        name="etiquette",
        description="Get the Venue Etiquette Guide.",
        contexts=[InteractionContextType.guild]
    )
    async def venue_etiquette(self, ctx: ApplicationContext) -> None:

        await self.bot.venue_etiquette(ctx.interaction)

################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Global(bot))

################################################################################
