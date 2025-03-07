from __future__ import annotations

import zoneinfo
import os
from datetime import timedelta
from typing import TYPE_CHECKING, Optional, Union

import cloudinary
import cloudinary.uploader
from discord import Bot, Attachment, Guild, NotFound, Member, User, Message, Interaction
from discord.abc import GuildChannel
from dotenv import load_dotenv
from discord.ext import tasks
import discord.utils

from Classes.BackgroundChecks.BGCheckManager import BGCheckManager
from Classes.Positions.PositionManager import PositionManager
from Classes.Venues.VenueManager import VenueManager
from Classes.XIVVenues.XIVVenuesClient import XIVVenuesClient
from Database.Database import Database
from .ChannelManager import ChannelManager
from .GuildManager import GuildManager
from .RoleManager import RoleManager
from .SPBLogger import SPBLogger
from Classes.Profiles.ProfileManager import ProfileManager
from Classes.Jobs.JobPostingManager import JobPostingManager
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import GuildData
################################################################################

__all__ = ("StaffPartyBot", )

################################################################################
class StaffPartyBot(Bot):

    IMAGE_DUMP = 991902526188302427
    SPB_ID = 1104515062187708525

    MAX_SELECT_OPTIONS = 25
    MAX_MULTI_SELECT_OPTIONS = 80

    load_dotenv()
    DEBUG = os.getenv("DEBUG") == "True"

    VENUE_ETIQUETTE = (
        "https://canary.discord.com/channels/955933227372122173/"
        "957656105092272208/1231769147113738260"
    )
    DE_ESCALATION = (
        "https://canary.discord.com/channels/955933227372122173/"
        "957656105092272208/1244338542029832333"
    )

################################################################################
    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self._img_dump: TextChannel = None  # type: ignore

        self._guild_mgr: GuildManager = GuildManager(self)
        self._db: Database = Database(self)
        self._xiv_client: XIVVenuesClient = XIVVenuesClient(self)
        self._logger: SPBLogger = SPBLogger(self)

        self._channel_mgr: ChannelManager = ChannelManager(self)
        self._role_mgr: RoleManager = RoleManager(self)

        self._position_mgr: PositionManager = PositionManager(self)
        self._venue_mgr: VenueManager = VenueManager(self)
        self._bg_check_mgr: BGCheckManager = BGCheckManager(self)
        self._profile_mgr: ProfileManager = ProfileManager(self)
        self._jobs_mgr: JobPostingManager = JobPostingManager(self)

################################################################################
    def __getitem__(self, guild_id: int) -> GuildData:

        return self._guild_mgr[guild_id]

################################################################################
    async def load_all(self) -> None:

        print("Loading dump channels...")
        self._img_dump = await self.fetch_channel(self.IMAGE_DUMP)
        print("Dump channels loaded.")

        print("Loading Cloudinary Client...")
        load_dotenv()
        cloudinary.config(
            cloud_name=os.getenv("CLOUD_NAME"),
            api_key=os.getenv("CLOUD_API_KEY"),
            api_secret=os.getenv("CLOUD_API_SECRET"),
            secure=True
        )

        payload = self.db.load_all()
        if not payload:
            raise Exception("No data found in the database.")

        print("Initializing logger...")
        await self._logger.load_all()

        print("Initializing guilds data...")
        # guild_ids = []
        # for guild in self.guilds:
        #     await self._guild_mgr.init_guild(guild)
        #     guild_ids.append(guild.id)
        #
        # for data in payload["guilds"]:
        #     guild_data = self[data["id"]]
        #     if guild_data is None:
        #         continue
        #     await guild_data.load_all(data["data"])
        #     guild_ids.remove(guild_data.guild_id)
        #
        # # Add any new guilds to the database
        # for gid in guild_ids:
        #     self.db.insert.guild(self.get_guild(gid))

        print("Loading channel & role managers...")
        self._channel_mgr.load_all(payload["channel_manager"])
        self._role_mgr.load_all(payload["role_manager"])

        print("Loading positions...")
        await self._position_mgr.load_all(payload["position_manager"])
        print("Loading venues...")
        await self._venue_mgr.load_all(payload["venue_manager"])
        print("Loading background checks...")
        await self._bg_check_mgr.load_all(payload["bg_check_manager"])
        print("Loading profiles...")
        await self._profile_mgr.load_all(payload["profile_manager"])
        print("Loading jobs...")
        await self._jobs_mgr.load_all(payload["jobs_manager"])

        print("Finalizing load...")
        await self._finalize_load()

        print("Done!")

################################################################################
    async def _finalize_load(self) -> None:

        for attr in self.__slots__:
            if attr.endswith("_mgr"):
                mgr = getattr(self, attr)
                if getattr(mgr, "finalize_load", None):
                    await mgr.finalize_load()

################################################################################
    @property
    def db(self) -> Database:

        return self._db

################################################################################
    @property
    def SPB_GUILD(self) -> Guild:

        return self.get_guild(self.SPB_ID)

################################################################################
    @property
    def guild_manager(self) -> GuildManager:

        return self._guild_mgr

################################################################################
    @property
    def xiv_client(self) -> XIVVenuesClient:

        return self._xiv_client

################################################################################
    @property
    def venue_manager(self) -> VenueManager:

        return self._venue_mgr

################################################################################
    @property
    def position_manager(self) -> PositionManager:

        return self._position_mgr

################################################################################
    @property
    def bg_check_manager(self) -> BGCheckManager:

        return self._bg_check_mgr

################################################################################
    @property
    def log(self) -> SPBLogger:

        return self._logger

################################################################################
    # Can't call this "channels" because that conflicts with the discord.py attribute
    @property
    def channel_manager(self) -> ChannelManager:

        return self._channel_mgr

################################################################################
    @property
    def role_manager(self) -> RoleManager:

        return self._role_mgr

################################################################################
    @property
    def profile_manager(self) -> ProfileManager:

        return self._profile_mgr

################################################################################
    @property
    def jobs_manager(self) -> JobPostingManager:

        return self._jobs_mgr

################################################################################
    async def dump_image(self, image: Attachment) -> str:

        file = await image.to_file()
        post = await self._img_dump.send(file=file)

        return post.attachments[0].url

################################################################################
    @staticmethod
    async def dump_image_cloudinary(image: Attachment) -> str:

        ret = cloudinary.uploader.upload(await image.read())
        return ret["secure_url"]

################################################################################
    async def add_guild(self, guild: Guild) -> None:

        if guild in self._guild_mgr:
            await self.register_commands(force=True, guild_id=guild.id)
            return

        await self._guild_mgr.init_guild(guild, True)

        exists = self.db.fetch_guild(guild.id)
        if not exists:
            self.db.insert.guild(self.get_guild(guild.id))

################################################################################
    async def get_or_fetch_channel(self, channel_id: int) -> Optional[GuildChannel]:

        ret = self.get_channel(channel_id)
        if ret is not None:
            return ret

        for guild in self.guilds:
            try:
                return await guild.fetch_channel(channel_id)
            except NotFound:
                continue

################################################################################
    async def get_or_fetch_role(self, role_id: int) -> Optional[GuildChannel]:

        ret = self.get_channel(role_id)
        if ret is not None:
            return ret

        for guild in self.guilds:
            try:
                return await guild._fetch_role(role_id)  # type: ignore
            except NotFound:
                continue

################################################################################
    async def get_or_fetch_member_or_user(self, user_id: int) -> Optional[Union[Member, User]]:

        for guild in self.guilds:
            if member := guild.get_member(user_id):
                return member

        try:
            return await self.fetch_user(user_id)
        except NotFound:
            return None

################################################################################
    async def get_or_fetch_message(self, message_url: str) -> Optional[Message]:

        url_parts = message_url.split("/")

        if message := self.get_message(int(url_parts[-1])):
            return message

        if channel := await self.get_or_fetch_channel(int(url_parts[-2])):
            try:
                return await channel.fetch_message(int(url_parts[-1]))  # type: ignore
            except NotFound:
                return None

################################################################################
    async def venue_etiquette(self, interaction: Interaction) -> None:

        await interaction.response.defer()

        etiquette_msg = await self.get_or_fetch_message(self.VENUE_ETIQUETTE)
        de_escalation_msg = await self.get_or_fetch_message(self.DE_ESCALATION)

        files = [
            await etiquette_msg.attachments[0].to_file(),
            await de_escalation_msg.attachments[0].to_file()
        ]

        await interaction.respond(files=files, delete_after=300)

################################################################################
    async def on_member_leave(self, member: Member) -> None:

        venue_deleted = await self.venue_manager.on_member_leave(member)
        profile_deleted = await self.profile_manager.on_member_leave(member)

        await self.log.on_member_leave(
            member=member,
            venue_deleted=venue_deleted,
            profile_deleted=profile_deleted,
            jobs_deleted=0,
            jobs_canceled=0
        )

################################################################################
    async def on_member_join(self, member: Member) -> None:

        await self.log.on_member_join(member)
        self.member_welcome.start(member)

################################################################################
    @tasks.loop(count=1)
    async def member_welcome(self, member: Member) -> None:

        welcome_channel = await self.channel_manager.welcome_channel
        if not welcome_channel:
            return

        welcome_message = (
            "# __Welcome to the <a:party_bus:1225557207836393645> "
            "Staff Party Bus!! <a:party_bus:1225557207836393645>__\n\n"

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
            if get_member := self.SPB_GUILD.get_member(member.id):
                member = get_member

            if await self.role_manager.venue_management_role in member.roles:
                welcome_message += (
                    "It looks like you've selected the Venue Management role!\n"
                    "You can follow the instructions <#1220087653815291954> to set up "
                    "your venue profile \\o/ <a:bartender:1168135253387378748> \n\n"
                )
                flag = True
            if await self.role_manager.staff_pending_role in member.roles:
                welcome_message += (
                    "I see you've picked the Staff Pending role!\n"
                    "You can follow the instructions here <#1104515062636478643> to do "
                    "your staff validation and you'll be able to create your staff "
                    "profile afterwards! <a:dancer:1168134583158575175>\n\n"
                )
                flag = True

            if flag:
                break
            else:
                attempts += 1

        if not flag:
            welcome_message += (
                "It looks like you haven't selected any roles yet! You can do so "
                "in <#1104515062636478638> to get started! <a:host:1168134582000943124>"
            )

        await welcome_channel.send(welcome_message)

################################################################################
