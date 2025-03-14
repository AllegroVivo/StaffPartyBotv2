from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional, List, Any, Dict, Union, Tuple
from zoneinfo import ZoneInfo

from discord import Embed, EmbedField, Interaction, User, SelectOption

from Assets import BotEmojis
from Enums import Timezone, Weekday, Hours, Position
from UI.Common import BasicTextModal, AccentColorModal, FroggeSelectView, TimeSelectView
from UI.Profiles import ProfileJobsModal, ProfileDetailsStatusView
from Utilities import Utilities as U, FroggeColor
from .Availability import Availability
from .ProfileSection import ProfileSection

if TYPE_CHECKING:
    from Classes import Profile
    from UI.Common import FroggeView
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
        self._color: Optional[FroggeColor] = (
            FroggeColor(kwargs.get("color"))
            if kwargs.get("color")
            else None
        )
        self._jobs: List[str] = kwargs.get("jobs", [])
        self._rates: Optional[str] = kwargs.get("rates")
        self._positions: List[Position] = [
            Position(pos_id)
            for pos_id
            in kwargs.get("position_ids", [])
        ]
        self._availability: List[Availability] = [
            Availability(self.parent, **a)
            for a in
            kwargs.get("availability", [])
        ]
        self._dm_pref: bool = kwargs.get("dm_pref", False)
        self._tz: Optional[ZoneInfo] = (
            ZoneInfo(kwargs.get("timezone"))
            if kwargs.get("timezone")
            else None
        )

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
    def positions(self, value: List[int]) -> None:

        self._positions = value
        self.update()

################################################################################
    @property
    def availability(self) -> List[Availability]:

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
    def timezone(self) -> Optional[ZoneInfo]:

        return self._tz

    @timezone.setter
    def timezone(self, value: Union[str, ZoneInfo]) -> None:

        if isinstance(value, str):
            value = ZoneInfo(value)

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
            "position_ids": [p.value for p in self._positions],
            "dm_pref": self._dm_pref,
            "timezone": self._tz.key if self._tz else None,
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
            ", ".join(f"`{p.proper_name}`" for p in self.positions[i:i+3])
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
                    value=Availability.short_availability_status(self._availability),
                    inline=False
                ),
                EmbedField("__Freelance Rates__", rates, False)
            ]
        )

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        return ProfileDetailsStatusView(user, self)

################################################################################
    def compile(self) -> Any:

        position_str = ", ".join([f"`{p.proper_name}`" for p in self.positions])
        availability = U.make_embed(
            color=self.color,
            title="__Availability__",
            description=(
                f"{Availability.long_availability_status(self.availability)}\n"

                "**__Employable Positions__**\n"
                f"{position_str}"
            ),
            footer_text=self._url
        )

        return (
            self.name,
            self.url,
            self.color,
            "/".join(self._jobs) if self._jobs else None,
            EmbedField(
                name=f"{BotEmojis.FlyingMoney} __Freelance Rates__ {BotEmojis.FlyingMoney}",
                value=(
                    f"{self.rates}\n"
                    f"{U.draw_line(extra=15)}"
                ),
                inline=False
            ) if self.rates else None,
            availability,
            self.dm_preference
        )

################################################################################
    def progress(self) -> str:

        return (
            f"{U.draw_line(extra=15)}\n"
            "__**Details**__\n"
            f"{self.progress_emoji(self._name)} -- Character Name\n"
            f"{self.progress_emoji(self._url)} -- Custom URL\n"
            f"{self.progress_emoji(self._color)} -- Accent Color\n"
            f"{self.progress_emoji(self._jobs)} -- Jobs List\n"
            f"{self.progress_emoji(self._rates)} -- Rates Field\n"
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
        await self.update_post_components()

################################################################################
    async def set_url(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Custom URL",
            attribute="Custom URL",
            cur_val=self._url,
            example="eg. 'https://carrd.co/AllegroVivo'",
            max_length=200,
            required=False
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
        await self.update_post_components()

################################################################################
    async def set_color(self, interaction: Interaction) -> None:

        modal = AccentColorModal(self.color)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.color = modal.value

################################################################################
    async def set_jobs(self, interaction: Interaction) -> None:

        modal = ProfileJobsModal(self.jobs)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.jobs = modal.value
        await self.update_post_components()

################################################################################
    async def set_rates(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Profile Rates Section",
            attribute="Rates Section",
            example="eg. '250k gil per photo shoot'",
            cur_val=self.rates,
            max_length=500,
            required=False,
            multiline=True
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.rates = modal.value
        await self.update_post_components()

################################################################################
    async def set_positions(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Set Positions",
            description="Please select the positions you are qualified to work."
        )
        view = FroggeSelectView(interaction.user, Position.select_options(), multi_select=True)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.positions = [Position(int(v)) for v in view.value]
        await self.update_post_components()

################################################################################
    async def set_timezone(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Set Timezone",
            description="Please select your timezone from the picker below."
        )
        view = FroggeSelectView(interaction.user, Timezone.select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.timezone = U.TIMEZONE_OFFSETS[Timezone(int(view.value))]

################################################################################
    async def toggle_dm_preference(self, interaction: Interaction) -> None:

        self.dm_preference = not self.dm_preference

        await interaction.edit()
        await self.update_post_components()

################################################################################
    async def set_availability(self, interaction: Interaction) -> None:

        if self._tz is None:
            await self.set_timezone(interaction)
            if self._tz is None:
                return

        prompt = U.make_embed(
            title="Set Availability",
            description="Please select the day you want to set availability for."
        )
        view = FroggeSelectView(interaction.user, Weekday.select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        weekday = Weekday(int(view.value))
        assert self._tz is not None

        prompt = U.make_embed(
            title="Set Availability Start",
            description=(
                f"Please select the beginning of your availability "
                f"for `{weekday.proper_name}`...\n\n"
                
                f"Times will be interpreted using the previously configured "
                f"`{self._tz.key}` timezone."
            )
        )
        view = TimeSelectView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        for i, a in enumerate(self._availability):
            if a.day == weekday:
                self._availability.pop(i).delete()
                break

        if view.value is Hours.Unavailable:
            return

        start_hour, start_minute = view.value

        prompt = U.make_embed(
            title="Set Availability End",
            description=(
                f"Please select the end of your availability "
                f"for `{weekday.proper_name}`...\n\n"

                f"Times will be interpreted using the previously configured "
                f"`{self._tz.key}` timezone."
            )
        )
        view = TimeSelectView(interaction.user, False)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        end_hour, end_minute = view.value

        # # === CONVERT USER INPUT TO UTC === #
        # today = datetime.today().date()  # Get today's date (we only care about time)
        #
        # # Create a naive datetime object
        # start_local = datetime(today.year, today.month, today.day, start_hour, start_minute)
        # end_local = datetime(today.year, today.month, today.day, end_hour, end_minute)
        #
        # # Attach the user's timezone
        # start_with_tz = start_local.replace(tzinfo=self._tz)
        # end_with_tz = end_local.replace(tzinfo=self._tz)
        #
        # # Convert to UTC
        # start_utc = start_with_tz.astimezone(ZoneInfo("UTC"))
        # end_utc = end_with_tz.astimezone(ZoneInfo("UTC"))
        #
        # # Store the UTC times
        # availability = Availability.new(
        #     self.parent, weekday, start_utc.hour,
        #     start_utc.minute, end_utc.hour, end_utc.minute
        # )
        # self._availability.append(availability)

        # 1) Figure out a date in local time for the chosen weekday
        #    This is optional, but if you want to handle the user picking e.g. "Wednesday"
        #    and it's currently "Sunday" in their local TZ, find the next Wednesday, etc.
        now_local = datetime.now(self._tz)
        today_local = now_local.date()
        # Python's datetime.weekday(): Monday=0..Sunday=6
        current_wkday = now_local.weekday()
        day_diff = (weekday.value - current_wkday) % 7
        chosen_date_local = today_local + timedelta(days=day_diff)

        # 2) Construct naive datetimes for the chosen date + user input hours/minutes
        start_naive = datetime(chosen_date_local.year, chosen_date_local.month, chosen_date_local.day,
                               start_hour, start_minute)
        end_naive = datetime(chosen_date_local.year, chosen_date_local.month, chosen_date_local.day,
                             end_hour, end_minute)

        # 3) Attach the user’s time zone (i.e., interpret these naive datetimes as local time)
        start_with_tz = start_naive.replace(tzinfo=self._tz)
        end_with_tz   = end_naive.replace(tzinfo=self._tz)

        # 4) Convert to UTC
        start_utc = start_with_tz.astimezone(ZoneInfo("UTC"))
        end_utc   = end_with_tz.astimezone(ZoneInfo("UTC"))

        # 5) Store the UTC times
        availability = Availability.new(
            self.parent,
            weekday,
            start_utc.hour,
            start_utc.minute,
            end_utc.hour,
            end_utc.minute
        )
        self._availability.append(availability)

        await self.update_post_components()

################################################################################
