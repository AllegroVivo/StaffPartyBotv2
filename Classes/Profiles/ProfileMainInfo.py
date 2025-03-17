from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional, List, Any, Dict, Union, Tuple
from zoneinfo import ZoneInfo

from discord import Embed, EmbedField, Interaction, User, SelectOption

from Assets import BotEmojis
from Enums import Timezone, Weekday, Hours, Position, XIVRegion, RPLevel, VenueTag
from UI.Common import BasicTextModal, FroggeSelectView, TimeSelectView, ConfirmCancelView
from UI.Profiles import ProfileDetailsStatusView
from Utilities import Utilities as U, FroggeColor
from .Availability import Availability
from .ProfileSection import ProfileSection

if TYPE_CHECKING:
    from Classes import Profile
    from UI.Common import FroggeView
################################################################################

__all__ = ("ProfileMainInfo",)

################################################################################
class ProfileMainInfo(ProfileSection):

    __slots__ = (
        "_name",
        "_regions",
        "_availability",
        "_dm_pref",
        "_tz",
        "_positions",
        "_trainings",
        "_rp_level",
        "_tags",
    )

################################################################################
    def __init__(self, parent: Profile, **kwargs) -> None:

        super().__init__(parent)

        self._name: Optional[str] = kwargs.get("name")
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
        self._regions: List[XIVRegion] = [XIVRegion(dc) for dc in kwargs.get("data_centers", [])]
        self._positions: List[Position] = [
            Position(pos_id)
            for pos_id
            in kwargs.get("position_ids", [])
        ]
        self._trainings: List[Position] = [
            Position(pos_id)
            for pos_id
            in kwargs.get("training_ids", [])
        ]
        self._rp_level: Optional[RPLevel] = (
            RPLevel(kwargs.get("rp_level"))
            if kwargs.get("rp_level")
            else None
        )
        self._tags: List[VenueTag] = [VenueTag(tag) for tag in kwargs.get("venue_tags", [])]

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
    def positions(self) -> List[Position]:

        self._positions.sort(key=lambda p: p.proper_name)
        return self._positions

    @positions.setter
    def positions(self, value: List[Position]) -> None:

        self._positions = value
        self.update()

################################################################################
    @property
    def trainings(self) -> List[Position]:

        self._trainings.sort(key=lambda p: p.proper_name)
        return self._trainings

    @trainings.setter
    def trainings(self, value: List[Position]) -> None:

        self._trainings = value
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
    @property
    def regions(self) -> List[XIVRegion]:

        return self._regions

    @regions.setter
    def regions(self, value: List[XIVRegion]) -> None:

        self._regions = value
        self.update()

################################################################################
    @property
    def rp_level(self) -> Optional[RPLevel]:

        return self._rp_level

    @rp_level.setter
    def rp_level(self, value: RPLevel) -> None:

        self._rp_level = value
        self.update()

################################################################################
    @property
    def preferred_tags(self) -> List[str]:

        return self._tags

    @preferred_tags.setter
    def preferred_tags(self, value: List[str]) -> None:

        self._tags = value
        self.update()

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "name": self._name,
            "position_ids": [p.value for p in self._positions],
            "training_ids": [t.value for t in self._trainings],
            "dm_pref": self._dm_pref,
            "timezone": self._tz.key if self._tz else None,
            "data_centers": [region.value for region in self._regions],
            "rp_level": self._rp_level.value if self._rp_level else None,
            "venue_tags": self._tags,
        }

################################################################################
    def status(self) -> Embed:

        # Group the positions in chunks, then join each chunk
        # with a comma and each group with "\n"
        def get_pos_str(positions: List[Position]) -> str:
            return "\n".join(
                ", ".join(f"`{p.proper_name}`" for p in positions[i:i+3])
                for i in range(0, len(positions), 3)
            ) if positions else "`Not Set`"

        position_str = get_pos_str(self.positions)
        training_str = get_pos_str(self.trainings)

        if self.trainings and self._rp_level is not None:
            training_str += (
                f"\n**Preferred RP Level:** `{self._rp_level.proper_name}`\n"
                f"**Desired Tags:** {', '.join([f'`{tag}`' for tag in self._tags])}"
            )

        name = f"`{str(self.name)}`" if self.name is not None else "`Not Set`"
        char_name = f"**Character Name:** {name}"

        return U.make_embed(
            title="Profile Main Information",
            color=self.accent_color,
            description=(
                f"{U.draw_line(text=char_name)}\n"
                f"{char_name}\n"
                f"{U.draw_line(text=char_name)}\n"
                "Select a button to add/edit the corresponding profile attribute."
            ),
            fields=[
                EmbedField("__Qualified Positions__", position_str, True),
                EmbedField("__Trainings Desired__", training_str, True),
                EmbedField(
                    name="__Home Region(s)__",
                    value=", ".join([f"`{r.proper_name}`" for r in self.regions]),
                    inline=False
                ),

                EmbedField(
                    name="__Availability__",
                    value=Availability.short_availability_status(self._availability),
                    inline=True
                ),
                EmbedField(
                    name="__DM Preference__",
                    value=U.yes_no_emoji(self._dm_pref),
                    inline=True
                ),
            ]
        )

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        return ProfileDetailsStatusView(user, self)

################################################################################
    def compile(self) -> Any:
        """Returns the Main Info data needed to create a profile post.

        Tuple returned represents the following:
        (name, regions, availability, dm_preference)

        Returns
        -------
        Tuple[str, str, Embed, bool]
        """

        region_str = f"{BotEmojis.World} __**Home Region(s)**__ {BotEmojis.World} \n"
        if self.regions:
            combined = "/".join([region.proper_name for region in self.regions])
            region_str += f"{combined}\n"
        else:
            region_str += "`Not Set`"

        def get_pos_str(positions: List[Position]) -> str:
            return "\n".join(
                ", ".join(f"`{p.proper_name}`" for p in positions[i:i + 3])
                for i in range(0, len(positions), 3)
            ) if positions else "`Not Set`"

        position_str = get_pos_str(self.positions)
        training_str = get_pos_str(self.trainings)

        availability = U.make_embed(
            color=self.accent_color,
            title="__Availability__",
            description=Availability.long_availability_status(self.availability),
            footer_text=self.custom_url,
            fields=[f for f in [
                EmbedField(
                    name="__Qualified Positions__",
                    value=position_str if position_str else "`Not Set`",
                    inline=True
                ) if self.positions else None,
                EmbedField(
                    name="__Trainings Desired__",
                    value=training_str if training_str else "`Not Set`",
                    inline=True
                ) if self.trainings else None
            ] if f is not None]
        )

        return self.name, region_str, availability, self.dm_preference
        
################################################################################
    def progress(self) -> str:

        return (
            f"{U.draw_line(extra=15)}\n"
            "__**Main Information**__\n"
            f"{self.progress_emoji(self._name)} -- Character Name\n"
            f"{self.progress_emoji(self._regions)} -- Home Regions\n"
            f"{self.progress_emoji(self._availability)} -- Availability\n"
            f"{self.progress_emoji(self._dm_pref)} -- Accepting Work-Based DMs\n"
            f"{self.progress_emoji(self._positions)} -- Qualified Positions\n"
            f"{self.progress_emoji(self._trainings)} -- Desired Trainings \n"
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
    async def set_positions(self, interaction: Interaction) -> None:

        staff_role = await self.bot.role_manager.staff_main_role
        if staff_role not in interaction.user.roles:
            bg_check = self.parent.bg_check
            if bg_check is None or not bg_check.approved:
                if bg_check is None or not bg_check.is_submitted:
                    await self.bot.bg_check_manager.start_bg_check(interaction)
                else:
                    prompt = U.make_embed(
                        title="Background Check Already Submitted",
                        description=(
                            "You have already submitted your background check.\n\n"
                            
                            "Please contact a staff member if you need to make changes.\n"
                            "Otherwise, you can continue setting your profile and you will\n"
                            "receive a DM when your background check is approved."
                        )
                    )
                    await interaction.respond(embed=prompt, ephemeral=True)
                return

        prompt = U.make_embed(
            title="Set Qualified Positions",
            description="Please select the positions you are qualified to work."
        )
        options = [SelectOption(label="None", value="None", description="This will deactivate all DMs.")]
        options.extend(Position.limited_select_options())
        view = FroggeSelectView(interaction.user, options, multi_select=True)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        if "None" in view.value:
            if len(view.value) > 1:
                error = U.make_error(
                    title="Invalid Selection",
                    message="You cannot select both `None` and other positions.",
                    solution="Please try again."
                )
                await interaction.respond(embed=error, ephemeral=True)
            else:
                self.positions = []
            return

        self.positions = [Position(int(v)) for v in view.value]
        await self.update_post_components()

################################################################################
    async def set_trainings(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Set Desired Trainings",
            description="Please select the positions you would like to train in."
        )
        options = [SelectOption(label="None", value="None", description="This will deactivate all DMs.")]
        options.extend(Position.select_options())
        view = FroggeSelectView(interaction.user, options, multi_select=True)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        if "None" in view.value:
            if len(view.value) > 1:
                error = U.make_error(
                    title="Invalid Selection",
                    message="You cannot select both `None` and other positions.",
                    solution="Please try again."
                )
                await interaction.respond(embed=error, ephemeral=True)
            else:
                self.trainings = []
            return

        trainings = [Position(int(v)) for v in view.value]
        pos_list = []
        for t in trainings:
            if t in self.positions:
                pos_list.append(t)

        if pos_list:
            pos_str = ", ".join([f"`{t.proper_name}`" for t in pos_list])
            warning = U.make_embed(
                color=FroggeColor.yellow(),
                title="Warning",
                description=(
                    "You have selected training for a position that you've\n"
                    "already also claimed a qualification for.\n\n"
                    
                    f"Overlapping Position(s):\n"
                    f"{pos_str}\n\n"
                    
                    "**Are you sure you want to proceed?**"
                )
            )
            view = ConfirmCancelView(interaction.user)

            await interaction.respond(embed=warning, view=view)
            await view.wait()

            if not view.complete or view.value is False:
                return

        prompt = U.make_embed(
            title="Internship Setup: RP Environment",
            description=(
                "Please select the RP environment style you would most like "
                "to train in."
            )
        )
        view = FroggeSelectView(interaction.user, RPLevel.select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.rp_level = RPLevel(int(view.value))

        prompt = U.make_embed(
            title="Internship Setup: Preferred Venue Tags",
            description=(
                "Please select all tags that interest you in terms of a "
                "venue for your internship.\n\n"
            )
        )
        view = FroggeSelectView(interaction.user, VenueTag.select_options())

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.preferred_tags = [VenueTag(int(tag)) for tag in view.value]

        self.trainings = trainings
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
    async def set_regions(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Select Your Home Region(s)",
            description=(
                "Pick your character's home region(s) from the drop-down below."
            )
        )
        view = FroggeSelectView(interaction.user, XIVRegion.select_options(), multi_select=True)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.regions = [XIVRegion(int(dc)) for dc in view.value]
        await self.update_post_components()

################################################################################
