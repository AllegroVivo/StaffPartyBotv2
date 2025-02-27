from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class Hours(FroggeEnum):

    Unavailable = -1
    TwelveAM = 0
    OneAM = 1
    TwoAM = 2
    ThreeAM = 3
    FourAM = 4
    FiveAM = 5
    SixAM = 6
    SevenAM = 7
    EightAM = 8
    NineAM = 9
    TenAM = 10
    ElevenAM = 11
    TwelvePM = 12
    OnePM = 13
    TwoPM = 14
    ThreePM = 15
    FourPM = 16
    FivePM = 17
    SixPM = 18
    SevenPM = 19
    EightPM = 20
    NinePM = 21
    TenPM = 22
    ElevenPM = 23

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == -1:
            return "Unavailable"

        hour = self.value % 12  # Convert 24-hour to 12-hour format
        hour = 12 if hour == 0 else hour  # Adjust for 12 AM / PM cases
        period = "AM" if self.value < 12 else "PM"

        return f"{hour}:xx {period}"

################################################################################
    @classmethod
    def limited_select_options(cls) -> List[SelectOption]:

        return [o.select_option() for o in cls if o != cls.Unavailable]

################################################################################
