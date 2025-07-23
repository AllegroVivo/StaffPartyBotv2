from typing import TYPE_CHECKING, Optional
from ._Enum import FroggeEnum

if TYPE_CHECKING:
    from Enums import DataCenter
################################################################################
class XIVRegion(FroggeEnum):

    North_America = 1
    Europe = 2
    Oceania = 3
    Japan = 4

################################################################################
    @property
    def proper_name(self) -> str:

        return self.name.replace("_",  " ")

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
    def contains(self, dc: "DataCenter") -> bool:

        if dc is None:
            return False

        if self.value == 1:
            return dc.value in [1, 2, 3, 4]
        elif self.value == 2:
            return dc.value in [5, 6]
        elif self.value == 3:
            return dc.value in [7]
        else:
            return dc.value in [8, 9, 10, 11]

################################################################################
    @classmethod
    def get_region_for_dc(cls, dc: "DataCenter") -> Optional["XIVRegion"]:

        for region in XIVRegion:
            if region.contains(dc):
                return region
        return None

################################################################################
