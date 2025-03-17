from __future__ import annotations

from typing import TYPE_CHECKING, List, Any, Dict, Optional

from discord import Embed, EmbedField, TextChannel, Interaction, ForumChannel, ChannelType

from Classes.Common import LazyChannel
from Enums import ChannelPurpose
from UI.Core import ChannelManagerMenuView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("ChannelManager", )

################################################################################
class ChannelManager:

    __slots__ = (
        "_state",
        "_venues",
        "_log",
        "_temp_jobs",
        "_perm_jobs",
        "_profiles",
        "_welcome",
        "_restart_notifs",
    )

################################################################################
    def __init__(self, state: StaffPartyBot) -> None:

        self._state: StaffPartyBot = state

        self._venues: LazyChannel = LazyChannel(self, None)
        self._log: LazyChannel = LazyChannel(self, None)
        self._temp_jobs: LazyChannel = LazyChannel(self, None)
        self._perm_jobs: LazyChannel = LazyChannel(self, None)
        self._profiles: LazyChannel = LazyChannel(self, None)
        self._welcome: LazyChannel = LazyChannel(self, None)
        self._restart_notifs: List[LazyChannel] = []

################################################################################
    def load_all(self, data: Dict[str, Any]) -> None:

        self._venues = LazyChannel(self, data.get("venue_channel_id"))
        self._log = LazyChannel(self, data.get("log_channel_id"))
        self._temp_jobs = LazyChannel(self, data.get("temp_job_channel_id"))
        self._perm_jobs = LazyChannel(self, data.get("perm_jobs_channel_id"))
        self._profiles = LazyChannel(self, data.get("profile_channel_id"))
        self._welcome = LazyChannel(self, data.get("welcome_channel_id"))
        self._restart_notifs = [
            LazyChannel(self, channel_id)
            for channel_id
            in data.get("restart_channel_ids", [])
        ]

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._state

################################################################################
    @property
    async def venue_post_channel(self) -> Optional[ForumChannel]:

        return await self._venues.get()

################################################################################
    @property
    async def log_channel(self) -> Optional[TextChannel]:

        return await self._log.get()

################################################################################
    @property
    async def temp_jobs_channel(self) -> Optional[ForumChannel]:

        return await self._temp_jobs.get()

    @property
    async def perm_jobs_channel(self) -> Optional[ForumChannel]:

        return await self._perm_jobs.get()

################################################################################
    @property
    async def profiles_channel(self) -> Optional[ForumChannel]:

        return await self._profiles.get()

################################################################################
    @property
    async def welcome_channel(self) -> Optional[TextChannel]:

        return await self._welcome.get()

################################################################################
    @property
    async def restart_notification_channels(self) -> List[TextChannel]:

        return [await channel.get() for channel in self._restart_notifs]

################################################################################
    def update(self) -> None:

        self._state.db.update.top_level(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "venue_channel_id": self._venues.id,
            "log_channel_id": self._log.id,
            "temp_job_channel_id": self._temp_jobs.id,
            "perm_jobs_channel_id": self._perm_jobs.id,
            "profile_channel_id": self._profiles.id,
            "welcome_channel_id": self._welcome.id,
            "restart_channel_ids": [channel.id for channel in self._restart_notifs],
        }

################################################################################
    async def status(self) -> Embed:

        venue_channel = await self.venue_post_channel
        log_channel = await self.log_channel
        profiles_channel = await self.profiles_channel
        temp_job_channel = await self.temp_jobs_channel
        perm_jobs_channel = await self.perm_jobs_channel
        welcome_channel = await self.welcome_channel
        restart_notifications = await self.restart_notification_channels

        def _mention(channel: Optional[TextChannel]) -> str:
            return channel.mention if channel else "`Not Set`"

        return U.make_embed(
            title="__Channels Status__",
            description=U.draw_line(extra=25),
            fields=[
                EmbedField(
                    name="__Welcome Channel__",
                    value=_mention(welcome_channel),
                    inline=False
                ),
                EmbedField(
                    name="__Log Stream__",
                    value=_mention(log_channel),
                    inline=False
                ),
                EmbedField(
                    name="__Staff Profiles__",
                    value=_mention(profiles_channel),
                    inline=False
                ),
                EmbedField(
                    name="__Venue Profiles__",
                    value=_mention(venue_channel),
                    inline=False
                ),
                EmbedField(
                    name="__Temporary Jobs__",
                    value=_mention(temp_job_channel),
                    inline=False
                ),
                EmbedField(
                    name="__Permanent Jobs__",
                    value=_mention(perm_jobs_channel),
                    inline=False
                ),
            ]
        )

################################################################################
    async def main_menu(self, interaction: Interaction) -> None:

        embed = await self.status()
        view = ChannelManagerMenuView(interaction.user, self)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    def get_channel(self, purpose: ChannelPurpose) -> LazyChannel:

        match purpose:
            case ChannelPurpose.LogStream:
                return self._log
            case ChannelPurpose.TempJobs:
                return self._temp_jobs
            case ChannelPurpose.PermJobs:
                return self._perm_jobs
            case ChannelPurpose.Venues:
                return self._venues
            case ChannelPurpose.Profiles:
                return self._profiles
            case ChannelPurpose.Welcome:
                return self._welcome
            case _:
                raise ValueError(f"Invalid channel purpose: {purpose}")

################################################################################
    async def set_channel(self, interaction: Interaction, _type: ChannelPurpose) -> None:

        restrictions = [ChannelType.forum] if _type in (
            ChannelPurpose.Venues, ChannelPurpose.Profiles,
            ChannelPurpose.TempJobs, ChannelPurpose.PermJobs,
        ) else [ChannelType.text]

        channel = await U.select_channel(
            interaction, self.bot, _type.proper_name, restrictions=restrictions
        )
        if channel is None:
            return

        match _type:
            case ChannelPurpose.Venues:
                assert isinstance(channel, ForumChannel)
                self._venues.set(channel)
            case ChannelPurpose.Profiles:
                assert isinstance(channel, ForumChannel)
                self._profiles.set(channel)
            case ChannelPurpose.LogStream:
                assert isinstance(channel, TextChannel)
                self._log.set(channel)
            case ChannelPurpose.TempJobs:
                assert isinstance(channel, ForumChannel)
                self._temp_jobs.set(channel)
            case ChannelPurpose.PermJobs:
                assert isinstance(channel, ForumChannel)
                self._perm_jobs.set(channel)
            case ChannelPurpose.Welcome:
                assert isinstance(channel, TextChannel)
                self._welcome.set(channel)
            case _:
                raise ValueError(f"Invalid ChannelPurpose: {_type}")

        embed = U.make_embed(
            title="Channel Set!",
            description=f"The {_type.proper_name} has been set to {channel.mention}!"
        )
        await interaction.respond(embed=embed, ephemeral=True)

################################################################################
    async def post_trainee_message(self, interaction: Interaction) -> None:
        """Go on, ask Alyah why this is here."""

        await self.bot.jobs_manager._trainee_msg.post(interaction)

################################################################################
