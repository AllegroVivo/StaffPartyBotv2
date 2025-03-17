from ._Enum import FroggeEnum
################################################################################
class VenueTag(FroggeEnum):

    Twitch_DJ = 1
    Nightclub = 2
    Bards = 3
    Lounge = 4
    Cafe = 5
    Tavern = 6
    Gambling = 7
    Bath_House = 8
    Restaurant = 9
    Casino = 10
    Den = 11
    Inn = 12
    Shop = 13
    Fightclub = 14
    Courtesans = 15
    Auction_House = 16
    Artists = 17
    LGBTQIA = 18
    VIP = 19
    
################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 18:
            return "LGBTQIA+"
        
        return self.name.replace("_", " ")
    
################################################################################
    