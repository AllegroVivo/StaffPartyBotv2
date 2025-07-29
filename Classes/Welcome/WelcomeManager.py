from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Optional

import discord
from discord import TextChannel, Member, Interaction
from discord.ext.tasks import loop

from Assets import BotEmojis

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("WelcomeManager", )

################################################################################
class WelcomeManager:

    def __init__(self, state: StaffPartyBot):

        self._state: StaffPartyBot = state

################################################################################
    @property
    async def channel(self) -> Optional[TextChannel]:

        return await self._state.channel_manager.welcome_channel

################################################################################
    @loop(count=1)
    async def welcome(self, member: Member) -> None:

        welcome_channel = await self.channel
        if welcome_channel is None:
            return

        welcome_message = (
            f"# __Welcome to the {BotEmojis.PartyBus} Staff Party Bus!! "
            f"{BotEmojis.PartyBus}__\n\n"

            f"Hiya, {member.mention}! I'm the Staff Party Bus, and I'm going to be "
            f"your stalwart companion throughout your time here!\n\n"

            "First off, head over to <#1397733438341120151> or <#1397737169975771206> "
            "to use my commands!\n\n"

            f"__**{BotEmojis.Bartender} Venue Management {BotEmojis.Bartender}**__\n"
            "Quickly get started by using the </venue profile:1399873580774330514> command.\n\n"

            f"__**{BotEmojis.FlyingMoney} Staff Members {BotEmojis.FlyingMoney}**__\n"
            "Want to get started working for a venue? You can use the "
            "</staff profile:1399873580774330513> command to create your profile.\n\n"

            f"__**{BotEmojis.MusicNote} DJs {BotEmojis.MusicNote}**__\n"
            "Looking for gigs? Create a customized </dj profile:1399873580774330509> "
            "for everyone to see!\n\n"

            "For further details on what we're all about or how to get started, "
            f"you can check out the <#1104515062187708534> and <#1104515062636478635> "
            f"channels! {BotEmojis.ThumbsUp}"
        )

        attempts = 0
        target_dt = member.joined_at
        while attempts < 5:
            target_dt += timedelta(minutes=1)
            # One minute for role selection
            await discord.utils.sleep_until(target_dt)

            # Get updated member object
            if get_member := self._state.SPB_GUILD.get_member(member.id):
                member = get_member

            if len(member.roles) == 1:
                attempts += 1
            else:
                break

            if attempts >= 5:
                return

        await welcome_channel.send(welcome_message)

################################################################################
