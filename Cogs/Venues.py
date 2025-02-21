from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType,
    InteractionContextType
)
from ._test import test_api_data_parsing

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################
class Venues(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################

    venues = SlashCommandGroup(
        name="venue",
        description="Commands for venue- and internship-related tasks and queries.",
        contexts=[InteractionContextType.guild]
    )

################################################################################
    @venues.command(
        name="import",
        description="Import a venue from the FFXIV Venues API."
    )
    async def venue_import(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the venue to import.",
            required=True
        )
    ) -> None:

        await self.bot.venue_manager.import_venue(ctx.interaction, name)

################################################################################
    @venues.command(name="test")
    async def test_cmd(self, ctx: ApplicationContext) -> None:

        await ctx.interaction.response.defer()
        await test_api_data_parsing(self.bot)
        await ctx.respond("Test complete.")

################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Venues(bot))

################################################################################
