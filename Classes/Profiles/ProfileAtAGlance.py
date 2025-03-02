from __future__ import annotations

import math
import re
from typing import TYPE_CHECKING, Dict, Any, Optional, List, Union

from discord import User, Embed, EmbedField, Interaction

from Assets import BotEmojis
from UI.Common import FroggeView, BasicTextModal, FroggeSelectView
from UI.Profiles import (
    GenderPronounView,
    RaceClanSelectView,
    OrientationSelectView,
    ProfileAAGStatusView,
)
from .ProfileSection import ProfileSection
from Enums import Gender, Pronoun, Race, Clan, Orientation, XIVRegion, FroggeEnum
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all__ = ("ProfileAtAGlance", )

################################################################################
class ProfileAtAGlance(ProfileSection):

    __slots__ = (
        "_gender",
        "_pronouns",
        "_race",
        "_clan",
        "_orientation",
        "_height",
        "_age",
        "_mare",
        "_data_centers",
    )

################################################################################
    def __init__(self, parent: Profile, **kwargs) -> None:

        super().__init__(parent)

        self._pronouns: List[Pronoun] = [Pronoun(p) for p in kwargs.get("pronouns", [])]

        try:
            self._gender: Optional[Union[Gender, str]] = Gender(int(kwargs.get("gender")))
        except (TypeError, ValueError):
            self._gender = kwargs.get("gender")

        try:
            self._race: Optional[Union[Race, str]] = Race(int(kwargs.get("race")))
        except (TypeError, ValueError):
            self._race = kwargs.get("race")

        try:
            self._clan: Optional[Union[Clan, str]] = Clan(int(kwargs.get("clan")))
        except (TypeError, ValueError):
            self._clan = kwargs.get("clan")

        try:
            self._orientation: Optional[Union[Orientation, str]] = kwargs.get("orientation")
        except (TypeError, ValueError):
            self._orientation = kwargs.get("orientation")

        self._height: Optional[int] = kwargs.get("height")
        self._age: Optional[str] = kwargs.get("age")
        self._mare: Optional[str] = kwargs.get("mare")
        self._data_centers: List[XIVRegion] = [XIVRegion(dc) for dc in kwargs.get("data_centers", [])]

################################################################################
    @property
    def gender(self) -> Optional[Union[Gender, str]]:

        return self._gender

    @gender.setter
    def gender(self, value: Optional[Union[Gender, str]]) -> None:

        self._gender = value
        self.update()

################################################################################
    @property
    def pronouns(self) -> List[Pronoun]:

        return self._pronouns

    @pronouns.setter
    def pronouns(self, value: List[Pronoun]) -> None:

        self._pronouns = value
        self.update()

################################################################################
    @property
    def race(self) -> Optional[Union[Race, str]]:

        return self._race

    @race.setter
    def race(self, value: Optional[Union[Race, str]]) -> None:

        self._race = value
        self.update()

################################################################################
    @property
    def clan(self) -> Optional[Union[Clan, str]]:

        return self._clan

    @clan.setter
    def clan(self, value: Optional[Union[Clan, str]]) -> None:

        self._clan = value
        self.update()

################################################################################
    @property
    def orientation(self) -> Optional[Union[Orientation, str]]:

        return self._orientation

    @orientation.setter
    def orientation(self, value: Optional[Union[Orientation, str]]) -> None:

        self._orientation = value
        self.update()

################################################################################
    @property
    def height(self) -> Optional[int]:

        return self._height

    @height.setter
    def height(self, value: Optional[int]) -> None:

        self._height = value
        self.update()

################################################################################
    @property
    def age(self) -> Optional[str]:

        return self._age

    @age.setter
    def age(self, value: Optional[str]) -> None:

        self._age = value
        self.update()

################################################################################
    @property
    def mare(self) -> Optional[str]:

        return self._mare

    @mare.setter
    def mare(self, value: Optional[str]) -> None:

        self._mare = value
        self.update()

################################################################################
    @property
    def data_centers(self) -> List[XIVRegion]:

        return self._data_centers

    @data_centers.setter
    def data_centers(self, value: List[XIVRegion]) -> None:

        self._data_centers = value
        self.update()

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        def get_dict_value(attr: Optional[FroggeEnum]) -> Any:
            return str(attr.value) if isinstance(attr, FroggeEnum) else attr

        return {
            "pronouns": [p.value for p in self._pronouns],
            "gender": get_dict_value(self._gender),
            "race": get_dict_value(self._race),
            "clan": get_dict_value(self._clan),
            "orientation": get_dict_value(self._orientation),
            "height": self._height,
            "age": self._age,
            "mare": self._mare,
            "data_center": [dc.value for dc in self._data_centers],
        }

################################################################################
    @staticmethod
    def get_attribute_str(attr: Any) -> str:

        if not attr:
            return "`Not Set`"
        elif isinstance(attr, FroggeEnum):
            return attr.proper_name
        elif isinstance(attr, int):
            return str(attr)
        elif isinstance(attr, str):
            return attr
        elif isinstance(attr, list):
            return "/".join([p.proper_name for p in attr])
        else:
            raise ValueError(f"Invalid attribute type: {type(attr)}")

################################################################################
    def format_height(self) -> str:

        if self.height is None:
            return "`Not Set`"

        inches = int(self._height / 2.54)
        feet = int(inches / 12)
        leftover = int(inches % 12)

        return f"{feet}' {leftover}\" (~{self.height} cm.)"

################################################################################
    def status(self) -> Embed:

        race_val = self.get_attribute_str(self.race)
        clan_val = self.get_attribute_str(self.clan)

        raceclan = f"{race_val}/{clan_val}"
        if isinstance(self.race, str) or isinstance(self.clan, str):
            raceclan += "\n*(Custom Value(s))*"

        gender_val = self.get_attribute_str(self.gender)
        pronoun_val = self.get_attribute_str(self.pronouns)

        gp_combined = f"{gender_val} -- *({pronoun_val})*"
        if isinstance(self.gender, str):
            gp_combined += "\n*(Custom Value)*"

        orientation_val = self.get_attribute_str(self.orientation)
        if isinstance(self.orientation, str):
            orientation_val += "\n*(Custom Value)*"

        height_val = self.format_height()
        age_val = self.get_attribute_str(self.age)
        mare_val = self.get_attribute_str(self.mare)
        dc_val = self.get_attribute_str(self.data_centers)

        fields = [
            EmbedField("__Home Regions__", dc_val, True),
            EmbedField("", U.draw_line(extra=30), False),
            EmbedField("__Race/Clan__", raceclan, True),
            EmbedField("__Gender/Pronouns__", gp_combined, True),
            EmbedField("", U.draw_line(extra=30), False),
            EmbedField("__Orientation__", orientation_val, True),
            EmbedField("__Mare ID__", mare_val, True),
            EmbedField("", U.draw_line(extra=30), False),
            EmbedField("__Height__", height_val, True),
            EmbedField("__RP Age__", age_val, True),
        ]

        return U.make_embed(
            color=self.parent.color,
            title=f"At A Glance Section Details for {self.parent.char_name}",
            description=(
                "*All sections, aside from **Home Region(s)** are optional.*\n"
                "*(Click the corresponding button below to edit each data point.)*\n"
                f"{U.draw_line(extra=38)}"
            ),
            fields=fields,
            timestamp=False
        )

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        return ProfileAAGStatusView(user, self)

################################################################################
    def _raw_string(self) -> str:

        ret = ""

        if self.data_centers:
            dcs = "/".join([dc.abbreviation for dc in self._data_centers])
            ret += f"__Home Region(s):__ {dcs}\n"

        if self.gender is not None:
            gender = self._gender.proper_name if isinstance(self._gender, Gender) else self._gender
            ret += f"__Gender:__ {gender}"

            if self.pronouns:
                pronouns = "/".join([p.proper_name for p in self._pronouns])
                ret += f" -- *({pronouns})*"

            ret += "\n"

        if self.race is not None:
            race = self._race.proper_name if isinstance(self._race, Race) else self._race
            ret += f"__Race:__ {race}"

            if self.clan is not None:
                clan = self._clan.proper_name if isinstance(self._clan, Clan) else self._clan
                ret += f" / {clan}"

            ret += "\n"

        if self.orientation is not None:
            orientation = (
                self._orientation.proper_name
                if isinstance(self._orientation, Orientation)
                else self._orientation
            )
            ret += f"__Orientation:__ {orientation}\n"

        if self.height is not None:
            ret += f"__Height:__ {self.format_height()}\n"

        if self.age is not None:
            ret += f"__RP Age:__ `{self.age}`\n"

        if self.mare is not None:
            ret += f"__Mare ID:__ `{self.mare}`\n"

        if ret:
            ret += U.draw_line(extra=15)

        return ret

################################################################################
    def compile(self) -> Any:

        if not self._raw_string():
            return None

        return EmbedField(
            name=f"{BotEmojis.Eyes} __At A Glance__ {BotEmojis.Eyes}",
            value=self._raw_string(),
            inline=False
        )

################################################################################
    def progress(self) -> str:

        return (
            f"{U.draw_line(extra=15)}\n"
            "__**At A Glance**__\n"
            f"{self.progress_emoji(self._data_centers)} -- Home Region(s)\n"
            f"{self.progress_emoji(self._gender)} -- Gender / Pronouns\n"
            f"{self.progress_emoji(self._race)} -- Race / Clan\n"
            f"{self.progress_emoji(self._orientation)} -- Orientation\n"
            f"{self.progress_emoji(self._height)} -- Height\n"
            f"{self.progress_emoji(self._age)} -- RP Age\n"
            f"{self.progress_emoji(self._mare)} -- Friend ID\n"
        )

################################################################################
    async def set_gender(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Gender/Pronoun Selection",
            description=(
                "Pick your preferred gender from the selector below.\n"
                "Don't worry,  you'll be able to choose your pronouns next!\n\n"

                "**If you select `Custom`, a pop-up will appear for you\n"
                "to provide your custom gender text.**"
            )
        )
        view = GenderPronounView(interaction.user, self)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.gender = view.value[0]
        self.pronouns = view.value[1]

################################################################################
    async def set_raceclan(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Select Your Race & Clan",
            description=(
                "Pick your character's race from the drop-down below.\n"
                "An additional selector will then appear for you to choose your clan.\n\n"

                "**If none of those apply, you may select `Custom`, and a pop-up will\n"
                "appear for you to enter your own custom information into.**"
            )
        )
        view = RaceClanSelectView(interaction.user, self)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.race = view.value[0]
        self.clan = view.value[1]

################################################################################
    async def set_orientation(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Select Your Orientation",
            description=(
                "Pick your preferred orientation from the selector below.\n\n"

                "**If you select `Custom`, a pop-up will appear for\n"
                "you to provide your custom orientation value.**"
            )
        )
        view = OrientationSelectView(interaction.user, self)

        await interaction.response.send_message(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        self.orientation = view.value

################################################################################
    async def set_height(self, interaction: Interaction) -> None:

        cur_val = None
        if self.height is not None:
            inches = int(self.height / 2.54)
            feet = int(inches / 12)
            leftover = int(inches % 12)
            cur_val = f"{feet}' {leftover}\""

        modal = BasicTextModal(
            title="Height Entry",
            attribute="Height",
            cur_val=cur_val,
            example="eg. '5'10\"' -or- '178 cm.'",
            max_length=20,
            required=False
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        raw = modal.value
        if raw is None:
            self.height = None
            return

        # RegEx Explanation: This RegEx pattern is designed to match a variety of
        # height input formats, including:
        # - A single number followed by "cm" or "cm."
        # - A single number followed by "ft", "feet", or "'"
        # - A single number followed by "in", "inches", or "'"
        # - A combination of the above three formats, separated by spaces
        result = re.match(
            r"^(\d+)\s*cm\.?|(\d+)\s*(?:ft\.?|feet|')$|(\d+)\s*(?:in\.?|inches|\"|'')|"
            r"(\d+)\s*(?:ft\.?|feet|')\s*(\d+)\s*(?:in\.?|inches|\"|'')",
            raw
        )

        if not result:
            error = U.make_error(
                title="Invalid Height Input",
                message=f"The value `{raw}` couldn't be interpreted.",
                solution=(
                    "The following are acceptable input styles:\n"
                    "- `X feet X inches`\n"
                    "- `X ft. X in.`\n"
                    "- `X in.`\n"
                    "- `X cm.`"
                )
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        if result.group(1):
            self.height = int(result.group(1))
        elif result.group(2):
            cm = int(result.group(2)) * 12 * 2.54
            self.height = math.ceil(cm)
        elif result.group(3):
            cm = int(result.group(3)) * 2.54
            self.height = math.ceil(cm)
        elif result.group(4) and result.group(5):
            inches = int(result.group(4)) * 12 + int(result.group(5))
            self.height = math.ceil(inches * 2.54)

################################################################################
    async def set_age(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Your RP Age",
            attribute="RP Age",
            cur_val=self.age,
            example="eg. '32' -or- 'Older than you think...'",
            max_length=30,
            required=False
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.age = modal.value

################################################################################
    async def set_mare(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Your Mare ID",
            attribute="Mare ID",
            cur_val=self.mare,
            example="eg. '1234567890'",
            max_length=30,
            required=False
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.mare = modal.value

################################################################################
    async def set_data_centers(self, interaction: Interaction) -> None:

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

        self.data_centers = [XIVRegion(int(dc)) for dc in view.value]

################################################################################
