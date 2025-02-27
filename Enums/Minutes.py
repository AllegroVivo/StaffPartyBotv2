from ._Enum import FroggeEnum
################################################################################
class Minutes(FroggeEnum):

    Zero = 0
    Fifteen = 1
    Thirty = 2
    FortyFive = 3

################################################################################
    @property
    def proper_name(self) -> str:

        return {
            0: "xx:00",
            1: "xx:15",
            2: "xx:30",
            3: "xx:45",
        }.get(self.value, "Unavailable")

################################################################################
