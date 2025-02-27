from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List, Any, Dict

from discord import Embed, EmbedField, Interaction

from Assets import BotEmojis
from UI.Common import BasicTextModal
from .ProfileSection import ProfileSection
from Utilities import Utilities as U, FroggeColor
from .PAvailability import PAvailability
from Enums import Timezone

if TYPE_CHECKING:
    from Classes import Profile, Position
################################################################################

__all__ = ("ProfileDetails", )

################################################################################
class ProfileDetails(ProfileSection):

    __slots__ = (
        "_name",
        "_url",
        "_color",
        "_jobs",
        "_rates",
        "_positions",
        "_availability",
        "_dm_pref",
        "_tz",
    )

################################################################################
    def __init__(self, parent: Profile, **kwargs) -> None:

        super().__init__(parent)

        self._name: Optional[str] = kwargs.get("name")
        self._url: Optional[str] = kwargs.get("url")
        self._color: FroggeColor = kwargs.get("color")
        self._jobs: List[str] = kwargs.get("jobs", [])
        self._rates: Optional[str] = kwargs.get("rates")
        self._positions: List[Position] = kwargs.get("positions", [])
        self._availability: List[PAvailability] = kwargs.get("availability", [])
        self._dm_pref: bool = kwargs.get("dm_pref", False)
        self._tz: Timezone = kwargs.get("timezone", Timezone.EST)

################################################################################
    def finalize_load(self) -> None:

        positions = [self.bot.position_manager[pos_id] for pos_id in self._positions]  # type: ignore
        self._positions = positions

################################################################################
    @property
    def name(self) -> str:

        return self._name or "Character Name Not Set"

    @name.setter
    def name(self, value: Optional[str]) -> None:

        self._name = value
        self.update()

################################################################################
    @property
    def url(self) -> Optional[str]:

        return self._url

    @url.setter
    def url(self, value: Optional[str]) -> None:

        self._url = value
        self.update()

################################################################################
    @property
    def color(self) -> Optional[FroggeColor]:

        return self._color

    @color.setter
    def color(self, value: Optional[FroggeColor]) -> None:

        self._color = value
        self.update()

################################################################################
    @property
    def jobs(self) -> List[str]:

        return self._jobs

    @jobs.setter
    def jobs(self, value: List[str]) -> None:

        self._jobs = value
        self.update()

################################################################################
    @property
    def rates(self) -> Optional[str]:

        return self._rates

    @rates.setter
    def rates(self, value: Optional[str]) -> None:

        self._rates = value
        self.update()

################################################################################
    @property
    def positions(self) -> List[Position]:

        return self._positions

    @positions.setter
    def positions(self, value: List[Position]) -> None:

        self._positions = value
        self.update()

################################################################################
    @property
    def availability(self) -> List[PAvailability]:

        self._availability.sort(key=lambda x: x.day.value)
        return self._availability

################################################################################
    @property
    def dm_preference(self) -> bool:

        return self._dm_pref

    @dm_preference.setter
    def dm_preference(self, value: bool) -> None:

        self._dm_pref = value
        self.update()

################################################################################
    @property
    def timezone(self) -> Timezone:

        return self._tz

    @timezone.setter
    def timezone(self, value: Timezone) -> None:

        self._tz = value
        self.update()

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "name": self._name,
            "url": self._url,
            "color": self._color.value if self._color else None,
            "jobs": self._jobs,
            "rates": self._rates,
            "positions": [p.id for p in self._positions],
            "dm_pref": self._dm_pref,
            "timezone": self._tz.value if self._tz else None,
        }

################################################################################
    def status(self) -> Embed:

        url_field = str(self.url) if self.url is not None else "`Not Set`"
        jobs = "- " + "\n- ".join(self._jobs) if self._jobs else "`Not Set`"
        rates = str(self.rates) if self.rates is not None else "`Not Set`"
        color_field = (
            f"{BotEmojis.ArrowLeft} -- (__{str(self.color).upper()}__)"
            if self._color is not None
            else "`Not Set`"
        )

        # Group the positions in chunks of 4, then join each chunk
        # with a comma and each group with "\n"
        positions = "\n".join(
            ", ".join(f"`{p.name}`" for p in self.positions[i:i+3])
            for i in range(0, len(self.positions), 3)
        ) if self.positions else "`Not Set`"

        name = f"`{str(self.name)}`" if self.name is not None else "`Not Set`"
        char_name = f"**Character Name:** {name}"

        return U.make_embed(
            title="Profile Details",
            color=self.color,
            description=(
                f"{U.draw_line(text=char_name)}\n"
                f"{char_name}\n"
                f"{U.draw_line(text=char_name)}\n"
                "Select a button to add/edit the corresponding profile attribute."
            ),
            fields=[
                EmbedField("__Color__", color_field, True),
                EmbedField("__RP Jobs__", jobs, True),
                EmbedField("__Custom URL__", url_field, False),
                EmbedField("__Employable Positions__", positions, True),
                EmbedField(
                    name="__DM Preference__",
                    value=(
                        f"{U.yes_no_emoji(self._dm_pref)}"
                        "*(This indicates whether\n"
                        "venue owners are encouraged\n"
                        "to DM you about work.)*"
                    ),
                    inline=True
                ),
                EmbedField(
                    name="__Availability__",
                    value=PAvailability.short_availability_status(self._availability),
                    inline=False
                ),
                EmbedField("__Freelance Rates__", rates, False)
            ]
        )

################################################################################
    async def set_name(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Character Name",
            attribute="Character Name",
            cur_val=self._name,
            example="eg. 'Allegro Vivo'",
            max_length=40
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.name = modal.value

################################################################################
    async def set_url(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Custom URL",
            attribute="Custom URL",
            cur_val=self._url,
            example="eg. 'https://carrd.co/AllegroVivo'",
            max_length=200
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        if not modal.value.startswith("https://"):
            error = U.make_error(
                title="Malformed URL",
                message=f"The URL '{modal.value}' is malformed and could not be accepted.",
                solution="Please ensure it is of schema '`https://`'."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        self.url = modal.value

################################################################################
    async def set_color(self, interaction: Interaction) -> None:

        modal = ProfileColorModal(self.color)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            log.debug("Profiles", "Color modal was not completed.")
            return

        self.color = Colour(modal.value)

################################################################################
