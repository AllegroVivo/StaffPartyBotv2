from __future__ import annotations

from typing import TYPE_CHECKING, List, Any, Dict, Optional

from discord import Embed, EmbedField, TextChannel, Interaction, ForumChannel, ChannelType, ComponentType

from Classes.Common import LazyChannel
from Enums import ChannelPurpose
from UI.Common import FroggeSelectView, ChannelSelectView
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
        "_internship",
        "_dj_profiles",
        "_special_events",
        "_services",
        "_communication"
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
        self._internship: LazyChannel = LazyChannel(self, None)
        self._dj_profiles: LazyChannel = LazyChannel(self, None)
        self._special_events: LazyChannel = LazyChannel(self, None)
        self._services: LazyChannel = LazyChannel(self, None)
        self._communication: LazyChannel = LazyChannel(self, None)

################################################################################
    def load_all(self, data: Dict[str, Any]) -> None:

        self._venues = LazyChannel(self, data.get("venue_channel_id"))
        self._log = LazyChannel(self, data.get("log_channel_id"))
        self._temp_jobs = LazyChannel(self, data.get("temp_job_channel_id"))
        self._perm_jobs = LazyChannel(self, data.get("perm_jobs_channel_id"))
        self._profiles = LazyChannel(self, data.get("profile_channel_id"))
        self._welcome = LazyChannel(self, data.get("welcome_channel_id"))
        self._internship = LazyChannel(self, data.get("group_training_channel_id"))
        self._dj_profiles = LazyChannel(self, data.get("bg_check_channel_id"))
        self._special_events = LazyChannel(self, data.get("special_event_channel_id"))
        self._services = LazyChannel(self, data.get("services_channel_id"))
        self._communication = LazyChannel(self, data.get("communication_channel_id"))

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
    async def internship_channel(self) -> Optional[TextChannel]:

        return await self._internship.get()

################################################################################
    @property
    async def dj_profiles_channel(self) -> Optional[TextChannel]:

        return await self._dj_profiles.get()

################################################################################
    @property
    async def special_events_channel(self) -> Optional[TextChannel]:

        return await self._special_events.get()

################################################################################
    @property
    async def services_channel(self) -> Optional[TextChannel]:

        return await self._services.get()

################################################################################
    @property
    async def communication_channel(self) -> Optional[TextChannel]:

        return await self._communication.get()

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
            "group_training_channel_id": self._internship.id,
            "bg_check_channel_id": self._dj_profiles.id,
            "special_event_channel_id": self._special_events.id,
            "services_channel_id": self._services.id,
            "communication_channel_id": self._communication.id,
        }

################################################################################
    async def status(self) -> Embed:

        venue_channel = await self.venue_post_channel
        log_channel = await self.log_channel
        profiles_channel = await self.profiles_channel
        temp_job_channel = await self.temp_jobs_channel
        perm_jobs_channel = await self.perm_jobs_channel
        welcome_channel = await self.welcome_channel
        internship_channel = await self.internship_channel
        dj_profiles_channel = await self.dj_profiles_channel
        special_event_channel = await self.special_events_channel
        services_channel = await self.services_channel
        communication_channel = await self.communication_channel

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
                EmbedField(
                    name="__Internship Channel__",
                    value=_mention(internship_channel),
                    inline=False
                ),
                EmbedField(
                    name="__DJ Profiles__",
                    value=_mention(dj_profiles_channel),
                    inline=False
                ),
                EmbedField(
                    name="__Special Events Channel__",
                    value=_mention(special_event_channel),
                    inline=False
                ),
                EmbedField(
                    name="__Services Channel__",
                    value=_mention(services_channel),
                    inline=False
                ),
                EmbedField(
                    name="__Communication Channel__",
                    value=_mention(communication_channel),
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
            case ChannelPurpose.Internship:
                return self._internship
            case ChannelPurpose.DJProfiles:
                return self._dj_profiles
            case ChannelPurpose.SpecialEvents:
                return self._special_events
            case ChannelPurpose.Services:
                return self._services
            case ChannelPurpose.Communication:
                return self._communication
            case _:
                raise ValueError(f"Invalid channel purpose: {purpose}")

################################################################################
    async def set_channel(self, interaction: Interaction, _type: ChannelPurpose) -> None:

        restrictions = [ChannelType.forum] if _type in (
            ChannelPurpose.Venues, ChannelPurpose.Profiles, ChannelPurpose.DJProfiles,
            ChannelPurpose.TempJobs, ChannelPurpose.PermJobs, ChannelPurpose.SpecialEvents,
            ChannelPurpose.Services
        ) else [ChannelType.text]

        prompt = U.make_embed(
            title="Select a Channel",
            description=f"Please select the channel for {_type.proper_name}."
        )
        view = ChannelSelectView(interaction.user, restrictions)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        channel = view.value

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
            case ChannelPurpose.Internship:
                assert isinstance(channel, TextChannel)
                self._internship.set(channel)
            case ChannelPurpose.DJProfiles:
                assert isinstance(channel, ForumChannel)
                self._dj_profiles.set(channel)
            case ChannelPurpose.SpecialEvents:
                assert isinstance(channel, ForumChannel)
                self._special_events.set(channel)
            case ChannelPurpose.Services:
                assert isinstance(channel, ForumChannel)
                self._services.set(channel)
            case ChannelPurpose.Communication:
                assert isinstance(channel, TextChannel)
                self._communication.set(channel)
            case _:
                raise ValueError(f"Invalid ChannelPurpose: {_type}")

        embed = U.make_embed(
            title="Channel Set!",
            description=f"The {_type.proper_name} has been set to {channel.mention}!"
        )
        await interaction.respond(embed=embed, ephemeral=True)

################################################################################
