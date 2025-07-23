from typing import List

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
    Host_Dancer = 8
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
    @classmethod
    def limited_select_options(cls, exclude: list) -> List[SelectOption]:

        return [p.select_option for p in cls if p not in exclude]

################################################################################
    @property
    def proper_name(self) -> str:

        return self.name.replace("_", " ")

################################################################################
    @property
    def description(self) -> str:

        if self.value == 0:
            ret = "Get general knowledge on venue environment and role particularities."
        elif self.value == 1:
            ret = "Provides theme-based or general music to entertain guest with a selection of songs."
        elif self.value == 2:
            ret = "Engage guests and serve drinks using emotes and role-play."
        elif self.value == 3:
            ret = "(NSFW) Offers scheduled erotic role-play services in a consensual environment."
        elif self.value == 4:
            ret = "Provide theme-based or general music in streams scheduled with management."
        elif self.value == 5:
            ret = "(NSFW) Offers lap dances in designated places with emotes and role-play conversation."
        elif self.value == 6:
            ret = "Offers various games of chance with set amounts of gils and house rules."
        elif self.value == 7:
            ret = "Gives patron venue information provided by venue management."
        elif self.value == 8:
            ret = "Engage guests; provide company and information about the venue."
        elif self.value == 9:
            ret = "Coordinate different levels of venue services and support staff, DJs and patrons."
        elif self.value == 10:
            ret = "Keeps up a scheduled party finder containing venue information provided by venue management."
        elif self.value == 11:
            ret = "Takes venue snap shots or more complex gpose of patrons to display in the venue discord."
        elif self.value == 12:
            ret = "Provide a safe, confidential space to promote an intimate scheduled companionship."
        elif self.value == 13:
            ret = "Can fill various roles. Maintains immersion and narrative while interacting with patrons"
        elif self.value == 14:
            ret = "Encourages proper venue etiquette while managing VIP (sales & services)."
        elif self.value == 15:
            ret = "Travels to each main city-state of each world to shout premade announcements."
        elif self.value == 16:
            ret = "Offers to read the drawn cards and provide insights about the possible meaning they hold."
        else:
            ret = "No description configured."

        return ret[:100]  # Limit description to 100 characters

################################################################################
