from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType,
    OptionChoice,
    guild_only,
)

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
        guild_only=True
    )

################################################################################
    @venues.command(
        name="import",
        description="Import a venue from the FFXIV Venues API."
    )
    @guild_only()
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
