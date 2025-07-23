from __future__ import annotations

from discord import Cog
from typing import TYPE_CHECKING, List
from discord.ext import tasks

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################
class Internal(Cog):

    def __init__(self, bot: StaffPartyBot):

        self.bot: StaffPartyBot = bot

################################################################################
    @Cog.listener("on_ready")
    async def load_internals(self) -> None:

        print("Loading internals...")
        await self.bot.load_all()

        print("Starting tasks...")
        self.manager_routines.start()
        self.clear_member_cache_routine.start()
        
        print(f"{self.bot.__class__.__name__} Online!")

################################################################################
    @Cog.listener("on_member_join")
    async def on_member_join(self, member) -> None:

        await self.bot.on_member_join(member)
        
################################################################################
    @Cog.listener("on_member_remove")
    async def on_member_remove(self, member) -> None:

        await self.bot.on_member_leave(member)
        
################################################################################
    @tasks.loop(minutes=5)
    async def clear_member_cache_routine(self) -> None:

        self.bot.clear_member_cache()

################################################################################
    @tasks.loop(minutes=1)
    async def manager_routines(self) -> None:

        await self.bot.jobs_manager.cull_postings()
        await self.bot.jobs_manager.check_revisits()

        await self.bot.services_manager.check_revisits()

################################################################################
    @tasks.loop(hours=24)
    async def update_xiv_venus(self) -> None:

        await self.bot.venue_manager.update_all_from_xiv()

################################################################################
def setup(bot: StaffPartyBot) -> None:

    bot.add_cog(Internal(bot))

################################################################################
