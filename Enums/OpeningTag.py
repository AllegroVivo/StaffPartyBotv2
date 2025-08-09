from ._Enum import FroggeEnum
################################################################################
class OpeningTag(FroggeEnum):

    Nightclub = 1
    Lounge = 2
    Cafe = 3
    Tavern = 4
    Bath_House = 5
    Restaurant = 6
    Casino = 7
    Den = 8
    Inn = 9
    Shop = 10
    Fight_Club = 11
    Auction_House = 12

################################################################################
    @property
    def proper_name(self) -> str:

        return self.name.replace("_", " ")

################################################################################
