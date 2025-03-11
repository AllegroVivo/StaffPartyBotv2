from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class Position(FroggeEnum):

    General_Training = 0
    Bard = 1
    Bartender = 2
    Courtesan = 3
    DJ = 4
    Exotic_Dancer = 5
    Gamba = 6
    Greeter = 7
    Host = 8
    Manager = 9
    PF_Attendant = 10
    Photographer = 11
    Pillow = 12
    RP_Flex = 13
    Security = 14
    Shout_Runner = 15
    Tarot_Reader = 16

################################################################################
    @property
    def select_option(self) -> SelectOption:

        return SelectOption(
            label=self.proper_name,
            value=str(self.value),
            description=self.description[:100]
        )

################################################################################
    @property
    def proper_name(self) -> str:

        return self.name.replace("_", " ")

################################################################################
    @property
    def description(self) -> str:

        if self.value == 0:
            return ""
        elif self.value == 1:
            return ""
        elif self.value == 2:
            return ""
        elif self.value == 3:
            return ""
        elif self.value == 4:
            return ""
        elif self.value == 5:
            return ""
        elif self.value == 6:
            return ""
        elif self.value == 7:
            return ""
        elif self.value == 8:
            return ""
        elif self.value == 9:
            return ""
        elif self.value == 10:
            return ""
        elif self.value == 11:
            return ""
        elif self.value == 12:
            return ""
        elif self.value == 13:
            return ""
        elif self.value == 14:
            return ""
        elif self.value == 15:
            return ""
        elif self.value == 16:
            return ""
        else:
            return "No description configured."

################################################################################
