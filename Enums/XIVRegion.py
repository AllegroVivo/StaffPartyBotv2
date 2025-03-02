from ._Enum import FroggeEnum
################################################################################
class XIVRegion(FroggeEnum):

    NorthAmerica = 1
    Europe = 2
    Oceana = 3
    Japan = 4

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 1:
            return "North America"

        return self.name

################################################################################
    @property
    def abbreviation(self) -> str:

        if self.value == 1:
            return "NA"
        elif self.value == 2:
            return "EU"
        elif self.value == 3:
            return "OC"
        elif self.value == 4:
            return "JP"

        return self.name
    
################################################################################
    