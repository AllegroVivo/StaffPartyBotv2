from ._Enum import FroggeEnum
################################################################################
class Minutes(FroggeEnum):

    Zero = 0
    Fifteen = 15
    Thirty = 30
    FortyFive = 45

################################################################################
    @property
    def proper_name(self) -> str:

        return f"xx:{self.value:02d}"

################################################################################
