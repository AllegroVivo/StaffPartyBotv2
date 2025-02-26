from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional

from discord import Embed, Message, TextChannel, User, EmbedField

from UI.BackgroundChecks import BGCheckApprovalView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import *
################################################################################

__all__ = ("SPBLogger", )

################################################################################
class SPBLogger:

    __slots__ = (
        "_state",
        "_alyah",
    )

################################################################################
    def __init__(self, state: StaffPartyBot) -> None:

        self._state: StaffPartyBot = state
        self._alyah: User = None  # type: ignore

################################################################################
    async def load_all(self) -> None:

        self._alyah = await self.bot.fetch_user(334530475479531520)

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._state

################################################################################
    @property
    async def log_channel(self) -> Optional[TextChannel]:

        return await self.bot.channel_manager.log_channel

################################################################################
    async def _log(self, message: Embed, **kwargs) -> Optional[Message]:

        channel = await self.log_channel
        if channel is None:
            return None

        return await channel.send(embed=message, **kwargs)

################################################################################
    async def venue_created(self, venue: Venue) -> None:

        users = "\n".join(
            [f"* {u.mention} ({u.display_name})"
             for u in await venue.managers]
        )

        embed = U.make_embed(
            title="Venue Created!",
            description=(
                f"New venue `{venue.name}` has been created!\n\n"

                f"__Managers:__\n"
                f"{users}"

            ),
            timestamp=True
        )

        await self._log(embed)
        if not self.bot.DEBUG:
            await self._alyah.send(embed=embed)

################################################################################
    async def bg_check_submitted(self, bg_check: BGCheck) -> Message:

        user = await bg_check.user
        embed = U.make_embed(
            title="Background Check Submitted!",
            description=(
                f"__**User:**__\n"
                f"{user.mention}\n"
                f"({user.display_name})\n"
            ),
            fields=[
                EmbedField(
                    name="__Names__",
                    value="- " + ("\n- ".join(bg_check.names)),
                    inline=True
                ),
                EmbedField(
                    name="__Venue Experience__",
                    value="\n".join([f'* {v.format()}' for v in bg_check.venues]),
                    inline=False
                )
            ],
            timestamp=True
        )
        view = BGCheckApprovalView(bg_check)

        msg = await self._log(embed, view=view)

        greetings = [
            "Hey Cutie!", "Hey Sexy!", "Hey Handsome!", "Hey Beautiful!",
            "Hey Gorgeous!", "Hey Stud!", "Hey Babe!", "Hey Love!",
            "Hey Sweetheart!", "Hey Darling!", "Hey Sugar!", "Hey Honey!",
            "Hey Sweetie!", "Hey Sunshine!", "Hey Angel!", "Hey Lovebug!",
            "Hey Snugglebug!", "Hey Cuddlebug!", "Hey Cutie Pie!",
            "Hey Cupcake!", "Hey Pumpkin!", "Hey Sweet Cheeks!",
            "Hey Sugar Lips!", "Hey Baby Cakes!", "Hey Doll Face!",
            "Hey Hot Stuff!", "Hey Hottie!", "Hey Sexy Pants!",
            "Hey Stud Muffin!", "Hey Love Muffin!", "Hey Sweet Thang!",
            "Hey Dreamboat!", "Hey Heartthrob!", "Hey Prince Charming!",
            "Hey Princess!", "Hey Queen!", "Hey King!", "Hey Prince!",
        ]
        closers = [
            "You should probably get on that.", "Time to hop into action.",
            "You should probably approve it.", "You should probably check it out.",
            "It's waiting for YOU!", "Get 'er done.", "You know what to do.",
            "You know the drill.", "You know the routine.", "You know the deal.",
            "Your mission, should you choose to accept it...", "It's your move.",
            "It's your turn.", "It's your time to shine.", "It's your time to act.",
        ]

        alert = U.make_embed(
            title="Background Check Submitted!",
            description=(
                f"{random.choice(greetings)} What up? There's a new BG check "
                f"waiting for you to approve it. {random.choice(closers)}\n\n"
    
                f"[Click here to see it!]({msg.jump_url})"
            ),
            timestamp=True
        )
        if not self.bot.DEBUG:
            await self._alyah.send(embed=alert)

        return msg

################################################################################
    async def bg_check_approved(self, bg_check: BGCheck) -> None:

        embed = U.make_embed(
            title="Background Check Approved!",
            description=(
                f"Background check for `{bg_check.names[0]}` has been approved!"
            ),
            timestamp=True
        )

        await self._log(embed)

################################################################################
    async def venue_removed(self, venue: Venue) -> None:

        embed = U.make_embed(
            title="Venue Removed!",
            description=(
                f"Venue `{venue.name}` has been removed from the system!"
            ),
            timestamp=True
        )

        await self._log(embed)

################################################################################
