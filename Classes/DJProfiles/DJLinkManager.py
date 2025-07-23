from __future__ import annotations

import hashlib
import re
from typing import TYPE_CHECKING, List, Optional
from urllib.parse import urlparse

from discord import Embed, Interaction, PartialEmoji, SelectOption

from Assets import BotEmojis
from Enums import LinkType
from Errors import MaxItemsReached
from UI.Common import BasicTextModal, FroggeSelectView
from UI.DJs import DJProfileLinksStatusView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import DJProfile
################################################################################

__all__ = ("DJLinkManager", )

################################################################################
class DJLinkManager:

    __slots__ = (
        "_parent",
        "_links"
    )

    MAX_LINKS = 20

################################################################################
    def __init__(self, parent: DJProfile, links: List[str]) -> None:

        self._parent: DJProfile = parent
        self._links: List[str] = links

################################################################################
    @property
    def links(self) -> List[str]:

        self._links.sort(key=lambda x: LinkType.identify_link_type(x).value)  # type: ignore
        return self._links

################################################################################
    @property
    def twitch_link(self) -> Optional[str]:

        return next(
            (l for l in self._links if LinkType.identify_link_type(l) == LinkType.Twitch),
            None
        )

################################################################################
    def status(self) -> Embed:

        return U.make_embed(
            color=self._parent.color,
            title="DJ Links Management",
            description=(
                f"**[`{len(self._links)}`] Links Registered**\n\n"
                
                f"{self.links_string()}"
            ),
        )

################################################################################
    async def menu(self, interaction: Interaction) -> None:

        embed = self.status()
        view = DJProfileLinksStatusView(interaction.user, self)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    def links_string(self) -> str:

        return "\n".join(self.links_list()) or "`Not Set`"

################################################################################
    def links_list(self) -> List[str]:

        links = []
        for link in self.links:
            link_type = LinkType.identify_link_type(link)
            link_name = (
                link_type.proper_name
                if link_type != LinkType.Other
                else self.extract_root_domain(link)
            )
            links.append(f"{self.get_emoji_for_link_type(link_type)} [{link_name}]({link})")

        return links

################################################################################
    @staticmethod
    def get_emoji_for_link_type(link_type: LinkType) -> PartialEmoji:

        match link_type:
            case LinkType.Carrd:
                return BotEmojis.CarrdLogo
            case LinkType.Discord:
                return BotEmojis.DiscordLogo
            case LinkType.Facebook:
                return BotEmojis.FacebookLogo
            case LinkType.Instagram:
                return BotEmojis.InstagramLogo
            case LinkType.Bluesky:
                return BotEmojis.BlueskyLogo
            case LinkType.YouTube:
                return BotEmojis.YouTubeLogo
            case LinkType.TikTok:
                return BotEmojis.TikTokLogo
            case LinkType.Twitch:
                return BotEmojis.TwitchLogo
            case LinkType.Spotify:
                return BotEmojis.SpotifyLogo
            case LinkType.SoundCloud:
                return BotEmojis.SoundCloudLogo
            case LinkType.Schedule:
                return BotEmojis.CalendarLogo
            case LinkType.Steam:
                return BotEmojis.SteamLogo
            case _:
                return BotEmojis.GenericLinkIcon

################################################################################
    @staticmethod
    def extract_root_domain(url: str) -> str:
        """
        Parses 'url' to extract the host (netloc), remove 'www.' if present,
        and then try to isolate a 'root' domain (e.g. 'example' from 'sub.example.co.uk').
        Returns the final piece capitalized, or an empty string if no domain found.
        """

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url  # add default scheme for parsing

        parsed = urlparse(url)
        # netloc is the host: e.g. 'www.example.com' or 'sub.example.co.uk'
        netloc = parsed.netloc or ""

        # In case there's a user:pass@host format
        if '@' in netloc:
            netloc = netloc.split('@', 1)[-1]

        # Remove a leading 'www.'
        if netloc.startswith("www."):
            netloc = netloc[4:]

        # If there's nothing left, bail out
        if not netloc:
            return ""

        # Split on dots, e.g. 'sub.example.co.uk' => ['sub','example','co','uk']
        parts = netloc.split('.')

        # If there's only 1 part, e.g. 'localhost' or 'example',
        # just use that as domain.
        if len(parts) == 1:
            return parts[0].capitalize()

        # For 2 or more parts, the last part is TLD (like 'com' or 'co.uk')
        # The second to last part is likely the "root" domain.
        # e.g. parts = ['sub','example','co','uk'] => root domain is 'example'
        # e.g. parts = ['example','com'] => root domain is 'example'
        # We'll pick parts[-2].
        root = parts[-2]
        return root.capitalize()

################################################################################
    async def add_link(self, interaction: Interaction) -> None:

        if len(self._links) >= self.MAX_LINKS:
            error = MaxItemsReached("DJ Links", self.MAX_LINKS)
            await interaction.respond(embed=error)
            return

        modal = BasicTextModal(
            title="Add DJ Link",
            attribute="Link URL",
            example="eg. 'https://example.com'",
            max_length=250
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        raw_link = modal.value
        proper_link = self.ensure_https(raw_link)

        if proper_link in self._links:
            error = U.make_error(
                title="Link Already Exists",
                message=f"DJ Link {modal.value.lower()} already exists on your profile.",
                solution="Please try again with a different link."
            )
            await interaction.respond(embed=error)
            return

        self._links.append(proper_link)

        self._parent.update()
        await self._parent.update_post_components()

################################################################################
    async def remove_link(self, interaction: Interaction) -> None:

        def short_hash_for_link(link: str, length: int = 8) -> str:
            """
            Returns a short string (up to 'length' hex digits)
            uniquely identifying the given link, using SHA256.
            """
            sha = hashlib.sha256(link.encode("utf-8")).hexdigest()
            return sha[:length]

        prompt = U.make_embed(
            color=self._parent.color,
            title="Remove DJ Link",
            description=(
                f"**[`{len(self._links)}`] Links Registered**\n\n"
                f"{self.links_string()}"
            ),
        )

        id_map = {}
        options = []
        for link in self._links:
            short_id = short_hash_for_link(link, length=8)
            id_map[short_id] = link
            label = U.string_clamp(link, 100)

            options.append(
                SelectOption(
                    label=label,
                    value=short_id,
                    emoji=self.get_emoji_for_link_type(LinkType.identify_link_type(link))
                )
            )

        view = FroggeSelectView(interaction.user, options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        real_link = id_map.get(view.value)
        if real_link and real_link in self._links:
            self._links.remove(real_link)

        self._parent.update()
        await self._parent.update_post_components()

################################################################################
    @staticmethod
    def ensure_https(url: str) -> str:
        """
        Returns 'url' with 'https://' prepended if it isn't already
        http:// or https://.
        """
        # Case-insensitive check for http or https at the beginning
        if not re.match(r'^(?:http|https)://', url, re.IGNORECASE):
            url = "https://" + url
        return url

################################################################################
