from ._Enum import FroggeEnum
################################################################################
class Service(FroggeEnum):

    ModDesigner = 1
    Artist = 2
    CarrdDeveloper = 3
    Crafter = 4
    DiscordAdmin = 5
    DJManager = 6
    GraphicDesigner = 7
    HousingDesigner = 8
    PublicRelations = 9
    PluginBotDeveloper = 10
    SocialMediaManager = 11
    VenueRental = 12
    Writer = 13
    GPoser = 14

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 1:
            return "Mod Designer"
        elif self.value == 3:
            return "Carrd Developer"
        elif self.value == 5:
            return "Discord Designer/Administrator"
        elif self.value == 6:
            return "DJ Manager/Administrator"
        elif self.value == 7:
            return "Graphic Designer"
        elif self.value == 8:
            return "Housing Designer"
        elif self.value == 9:
            return "Public Relations"
        elif self.value == 10:
            return "Plugin/Bot Developer"
        elif self.value == 11:
            return "Social Media Manager"
        elif self.value == 12:
            return "Venue Rental"
        else:
            return self.name

################################################################################
