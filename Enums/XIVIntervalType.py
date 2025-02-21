from ._Enum import FroggeEnum
################################################################################
class XIVIntervalType(FroggeEnum):

    EveryXWeeks = 0
    EveryXthDayOfTheMonth = 1

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 0:
            return "Every X Weeks"
        elif self.value == 1:
            return "Every Xth Day of the Month"

        return self.name
    
################################################################################
    