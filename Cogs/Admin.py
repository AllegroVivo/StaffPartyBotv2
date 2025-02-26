from typing import TYPE_CHECKING

from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType,
    InteractionContextType,
    ChannelType,
    OptionChoice
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
        name="channels",
        description="Set channels for server operations."
    )
    async def set_channels(self, ctx: ApplicationContext) -> None:

        await self.bot.channel_manager.main_menu(ctx.interaction)

################################################################################
    @admin.command(
        name="roles",
        description="Set roles for server operations."
    )
    async def set_roles(self, ctx: ApplicationContext) -> None:

        await self.bot.role_manager.main_menu(ctx.interaction)

################################################################################
    @admin.command(
        name="positions",
        description="Manage the position system for the server."
    )
    async def admin_positions(self, ctx: ApplicationContext) -> None:

        await self.bot.position_manager.main_menu(ctx.interaction)

################################################################################
    @admin.command(
        name="yeet_venue",
        description="Remove a venue from the system."
    )
    async def yeet_venue(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the venue to remove.",
            required=True
        )
    ) -> None:

        await self.bot.venue_manager.remove_venue(ctx.interaction, name)

################################################################################
    @admin.command(
        name="staff_experience",
        description="View a previously submitted staff background check."
    )
    async def staff_experience(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user to view the background check for.",
            required=True
        )
    ) -> None:

        await self.bot.bg_check_manager.staff_experience(ctx.interaction, user)

################################################################################


################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Admin(bot))

################################################################################
