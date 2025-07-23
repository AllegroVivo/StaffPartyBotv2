import re
from typing import TypeVar, Type
from ._Enum import FroggeEnum
################################################################################

DLT = TypeVar("DLT", bound="DJLinkType")

################################################################################
class LinkType(FroggeEnum):

    Twitch = 0
    Schedule = 1
    Discord = 2
    Bluesky = 3
    SoundCloud = 4
    Spotify = 5
    YouTube = 6
    TikTok = 7
    Instagram = 8
    Carrd = 9
    Facebook = 10
    Steam = 11

    Other = 25
    
################################################################################
    @property
    def proper_name(self) -> str:

        return self.name

################################################################################
    @staticmethod
    def identify_link_type(url: str) -> DLT:
        """
        Returns the DJLinkType enum value corresponding to the given 'url'.
        If none match, returns DJLinkType.Other.
        """
        for link_type, pattern in PATTERNS:
            if pattern.match(url):
                return link_type
        return LinkType.Other

################################################################################

PATTERNS = [
    (
        LinkType.Carrd,
        re.compile(r"^https?://(?:[\w-]+\.)*carrd\.co\S*$", flags=re.IGNORECASE)
    ),
    (
        LinkType.Discord,
        re.compile(r"^https?://(?:discord\.(?:gg|com|me)|discordapp\.com)\S*$", flags=re.IGNORECASE)
    ),
    (
        LinkType.Facebook,
        re.compile(r"^https?://(?:www\.)?(?:facebook\.com|fb\.com|fb\.me)\S*$", flags=re.IGNORECASE)
    ),
    (
        LinkType.Instagram,
        re.compile(r"^https?://(?:www\.)?(?:instagram\.com|instagr\.am)\S*$", flags=re.IGNORECASE)
    ),
    (
        LinkType.Bluesky,
        re.compile(r"^https?://(?:www\.)?bsky\.app/profile/[\w.-]+(?:/post/\w+)?/?$", flags=re.IGNORECASE)
    ),
    (
        LinkType.YouTube,
        re.compile(r"^https?://(?:www\.)?(?:youtube\.com|youtu\.be)\S*$", flags=re.IGNORECASE)
    ),
    (
        LinkType.TikTok,
        re.compile(r"^https?://(?:vm\.)?tiktok\.com\S*$", flags=re.IGNORECASE)
    ),
    (
        LinkType.Twitch,
        re.compile(r"^https?://(?:www\.)?twitch\.tv\S*$", flags=re.IGNORECASE)
    ),
    (
        LinkType.Spotify,
        re.compile(r"^https?://(?:open\.spotify\.com|spotify\.link)\S*$", flags=re.IGNORECASE)
    ),
    (
        LinkType.SoundCloud,
        re.compile(r"^https?://(?:soundcloud\.com|snd\.sc)\S*$", flags=re.IGNORECASE)
    ),
    (
        LinkType.Schedule,
        # If you just need any link containing "schedule" or "youcanbookme"
        re.compile(
            r'''^https?://(
                # 1) Google Calendar: "calendar.google.com" or "google.com/calendar"
                [^/]*google\.com/[^/]*calendar
                |
                # 2) YouCanBook.me: 
                (?:[\w-]+\.)?youcanbook\.me
                |
                # 3) ANY link that has "schedule" or "bookme" in its path/query
                \S*(?:schedule|bookme)\S*
            )\S*$''',
            re.IGNORECASE | re.VERBOSE
        )
    ),
    (
        LinkType.Steam,
        # Combining store.steampowered.com, steamcommunity.com, and s.team
        re.compile(
            r"^https?://(?:(?:store\.)?steampowered\.com|steamcommunity\.com|s\.team)\S*$",
            flags=re.IGNORECASE
        )
    ),
]

################################################################################
