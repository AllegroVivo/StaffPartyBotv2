from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType,
    InteractionContextType, ChannelType
)
from ._test import test_api_data_parsing

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################
class Admin(Cog):

    def __init__(self, bot: "StaffPartyBot"):

        self.bot: "StaffPartyBot" = bot

################################################################################

    admin = SlashCommandGroup(
        name="admin",
        description="Administrator commands for user/system configuration & management.",
        contexts=[InteractionContextType.guild]
    )

################################################################################
    @admin.command(
        name="import_venue",
        description="Import a new venue into the system."
    )
    async def import_venue(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the venue.",
            required=True
        ),
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="One of the venue's Owner/Manager contacts.",
            required=True
        )
    ) -> None:

        await self.bot.venue_manager.import_venue(ctx.interaction, name, user)

################################################################################
    @admin.command(
        name="set_log_channel",
        description="Set the logging channel for the server."
    )
    async def set_log_channel(
        self,
        ctx: ApplicationContext,
        channel: Option(
            SlashCommandOptionType.channel,
            name="channel",
            description="The channel to set as the logging channel.",
            required=True,
            channel_types=[ChannelType.text]
        )
    ) -> None:

        await self.bot.log.set_log_channel(ctx.interaction, channel)

################################################################################
    @admin.command(name="test")
    async def test_cmd(self, ctx: ApplicationContext) -> None:

        await ctx.interaction.response.defer()
        await test_api_data_parsing(self.bot)
        await ctx.respond("Test complete.")

################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Admin(bot))

################################################################################
