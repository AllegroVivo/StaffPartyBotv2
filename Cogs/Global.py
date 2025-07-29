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
    )
    async def help_menu(self, ctx: ApplicationContext) -> None:

        if not self.bot.is_loaded(ctx.interaction):
            return

        await HelpMessage(self.bot).menu(ctx.interaction)

################################################################################
    @slash_command(
        name="etiquette",
        description="Get the Venue Etiquette Guide.",
    )
    async def venue_etiquette(self, ctx: ApplicationContext) -> None:

        if not self.bot.is_loaded(ctx.interaction):
            return

        await self.bot.venue_etiquette(ctx.interaction)

################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Global(bot))

################################################################################
