import re
from ._Enum import FroggeEnum
################################################################################
class MusicGenre(FroggeEnum):

    BeatBass = 0
    Breakbeat = 1
    Country = 2
    DrumBass = 3
    Dubstep = 4
    Electro = 5
    ElectroSwing = 6
    Garage = 7
    HardDance = 8
    House = 9
    JazzBlues = 10
    KJPop = 11
    KJRock = 12
    LatinSpanish = 13
    Lofi = 14
    Lewdcore = 15
    Midtempo = 16
    PhonkTrap = 17
    Pop = 18
    RapHipHop = 19
    RockMetal = 20
    Mashup = 21
    Techno = 22
    ThemeMashup = 23
    Trance = 24
    
################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 0:
            return "Beat/Bass"
        elif self.value == 3:
            return "Drum & Bass"
        elif self.value == 10:
            return "Jazz/Blues"
        elif self.value == 11:
            return "K/J-Pop"
        elif self.value == 12:
            return "K/J-Rock"
        elif self.value == 13:
            return "Latin/Spanish"
        elif self.value == 17:
            return "Phonk/Trap"
        elif self.value == 19:
            return "Rap/Hip-Hop"
        elif self.value == 20:
            return "Rock/Metal"
        elif self.value == 23:
            return "Theme Mashup"

        return re.sub(r'([A-Z])', r' \1', self.name)

################################################################################
