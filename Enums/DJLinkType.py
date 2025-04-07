import re
from typing import TypeVar, Type
from ._Enum import FroggeEnum
################################################################################

DLT = TypeVar("DLT", bound="DJLinkType")

################################################################################
class DJLinkType(FroggeEnum):

    Twitch = 0
    Schedule = 1
    Discord = 2
    Twitter = 3
    SoundCloud = 4
    Spotify = 5
    YouTube = 6
    TikTok = 7
    Instagram = 8
    Carrd = 9
    Facebook = 10
    Steam = 11
    Other = 12
    
################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 3:
            return "Twitter/X"

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
        return DJLinkType.Other

################################################################################

PATTERNS = [
    (
        DJLinkType.Carrd,
        re.compile(r"^https?://(?:[\w-]+\.)*carrd\.co\S*$", flags=re.IGNORECASE)
    ),
    (
        DJLinkType.Discord,
        re.compile(r"^https?://(?:discord\.(?:gg|com|me)|discordapp\.com)\S*$", flags=re.IGNORECASE)
    ),
    (
        DJLinkType.Facebook,
        re.compile(r"^https?://(?:www\.)?(?:facebook\.com|fb\.com|fb\.me)\S*$", flags=re.IGNORECASE)
    ),
    (
        DJLinkType.Instagram,
        re.compile(r"^https?://(?:www\.)?(?:instagram\.com|instagr\.am)\S*$", flags=re.IGNORECASE)
    ),
    (
        DJLinkType.Twitter,
        # Common for X/Twitter includes x.com, twitter.com, t.co
        re.compile(r"^https?://(?:x\.com|twitter\.com|t\.co)\S*$", flags=re.IGNORECASE)
    ),
    (
        DJLinkType.YouTube,
        re.compile(r"^https?://(?:www\.)?(?:youtube\.com|youtu\.be)\S*$", flags=re.IGNORECASE)
    ),
    (
        DJLinkType.TikTok,
        re.compile(r"^https?://(?:vm\.)?tiktok\.com\S*$", flags=re.IGNORECASE)
    ),
    (
        DJLinkType.Twitch,
        re.compile(r"^https?://(?:www\.)?twitch\.tv\S*$", flags=re.IGNORECASE)
    ),
    (
        DJLinkType.Spotify,
        re.compile(r"^https?://(?:open\.spotify\.com|spotify\.link)\S*$", flags=re.IGNORECASE)
    ),
    (
        DJLinkType.SoundCloud,
        re.compile(r"^https?://(?:soundcloud\.com|snd\.sc)\S*$", flags=re.IGNORECASE)
    ),
    (
        DJLinkType.Schedule,
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
        DJLinkType.Steam,
        # Combining store.steampowered.com, steamcommunity.com, and s.team
        re.compile(
            r"^https?://(?:(?:store\.)?steampowered\.com|steamcommunity\.com|s\.team)\S*$",
            flags=re.IGNORECASE
        )
    ),
]

################################################################################
