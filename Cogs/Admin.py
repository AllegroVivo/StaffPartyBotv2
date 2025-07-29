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
        name="channels",
        description="Set channels for server operations."
    )
    async def set_channels(self, ctx: ApplicationContext) -> None:

        if not self.bot.is_loaded(ctx.interaction):
            return

        await self.bot.channel_manager.main_menu(ctx.interaction)

################################################################################
    @admin.command(
        name="roles",
        description="Set roles for server operations."
    )
    async def set_roles(self, ctx: ApplicationContext) -> None:

        if not self.bot.is_loaded(ctx.interaction):
            return

        await self.bot.role_manager.main_menu(ctx.interaction)

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

        if not self.bot.is_loaded(ctx.interaction):
            return

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

        if not self.bot.is_loaded(ctx.interaction):
            return

        await self.bot.bg_check_manager.staff_experience(ctx.interaction, user)

################################################################################
def setup(bot: "StaffPartyBot") -> None:

    bot.add_cog(Admin(bot))

################################################################################
