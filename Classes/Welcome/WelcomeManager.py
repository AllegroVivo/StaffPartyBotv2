from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Optional

import discord
from discord import TextChannel, Member
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

            f"Hiya, {member.mention}! I'm the Staff Party Bot, and I'm going to be "
            f"your best friend throughout your time here at the Staff Party Bus!\n\n"
        )

        flag = False
        attempts = 0
        target_dt = member.joined_at
        while attempts < 5:
            target_dt += timedelta(minutes=1)
            # One minute for role selection
            await discord.utils.sleep_until(target_dt)

            # Get updated member object
            if get_member := self._state.SPB_GUILD.get_member(member.id):
                member = get_member

            venue_management_role = await self._state.role_manager.venue_management_role
            if venue_management_role in member.roles:
                welcome_message += (
                    "It looks like you've selected the Venue Management role!\n"
                    "You can follow the instructions <#1220087653815291954> to set up "
                    f"your venue profile \\o/ {BotEmojis.Bartender} \n\n"
                )
                flag = True

            staff_pending = await self._state.role_manager.staff_pending_role
            if staff_pending in member.roles:
                welcome_message += (
                    "I see you've picked the Staff Pending role!\n"
                    "You can follow the instructions here <#1104515062636478643> to do "
                    "your staff validation and you'll be able to create your staff "
                    f"profile afterwards! {BotEmojis.Dancer}\n\n"
                )
                flag = True
            if "trainee" in [r.name.lower() for r in member.roles]:
                welcome_message += (
                    "I see you've selected the Trainee role!\n"
                    "You can follow the instructions here <#1219488746664230974> to "
                    f"set up your profile and receive training! {BotEmojis.Greeter}"
                )
                flag = True

            if flag:
                break
            else:
                attempts += 1

        if not flag:
            welcome_message += (
                "It looks like you haven't selected any roles yet! You can do so "
                f"in <#1104515062636478638> to get started! {BotEmojis.Host}"
            )

        await welcome_channel.send(welcome_message)

################################################################################
