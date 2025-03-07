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
class Venues(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################

    venues = SlashCommandGroup(
        name="venue",
        description="Commands for venue- and internship-related tasks and queries.",
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

        await self.bot.venue_manager.import_venue(ctx.interaction, name, None)

################################################################################
    @venues.command(
        name="toggle_user_mute",
        description="Toggle whether a user will hear about a venue's job postings.",
        contexts=[InteractionContextType.guild]
    )
    async def venue_toggle_user_mute(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="venue_name",
            description="The name of the venue to mute the user for.",
            required=True
        ),
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user to un/mute.",
            required=True
        )
    ) -> None:

        await self.bot.venue_manager.toggle_user_mute(ctx.interaction, name, user)

################################################################################
    @venues.command(
        name="profile",
        description="View and edit your venue's internship profile & status.",
        contexts=[InteractionContextType.guild]
    )
    async def venue_profile(self, ctx: ApplicationContext) -> None:

        await self.bot.venue_manager.venue_menu(ctx.interaction)

################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Venues(bot))

################################################################################
