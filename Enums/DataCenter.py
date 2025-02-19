from typing import Optional

from .GameWorld import GameWorld
from ._Enum import FroggeEnum
################################################################################
class DataCenter(FroggeEnum):
    
    Aether = 1
    Crystal = 2
    Dynamis = 3
    Primal = 4
    Light = 5
    Chaos = 6
    Materia = 7
    Elemental = 8
    Gaia = 9
    Mana = 10
    Meteor = 11

################################################################################
    @classmethod
    def from_xiv(cls, xiv_name: Optional[str]) -> Optional["DataCenter"]:
        
        if xiv_name is None:
            return None
        
        for dc in cls:
            if dc.proper_name == xiv_name:
                return dc
            
        raise ValueError(f"Invalid XIV data center name: {xiv_name}")
    
################################################################################
    @classmethod
    def from_world(cls, world: GameWorld) -> "DataCenter":
        
        if world in (
            GameWorld.Adamantoise, GameWorld.Cactuar, GameWorld.Faerie,
            GameWorld.Gilgamesh, GameWorld.Jenova, GameWorld.Midgardsormr,
            GameWorld.Sargatanas, GameWorld.Siren
        ):
            return cls.Aether
        
        if world in (
            GameWorld.Balmung, GameWorld.Brynhildr, GameWorld.Coeurl,
            GameWorld.Diabolos, GameWorld.Goblin, GameWorld.Malboro,
            GameWorld.Mateus, GameWorld.Zalera
        ):
            return cls.Crystal
        
        if world in (
            GameWorld.Cuchulainn, GameWorld.Golem, GameWorld.Halicarnassus,
            GameWorld.Kraken, GameWorld.Maduin, GameWorld.Marilith,
            GameWorld.Rafflesia, GameWorld.Seraph
        ):
            return cls.Dynamis
        
        if world in (
            GameWorld.Behemoth, GameWorld.Excalibur, GameWorld.Exodus,
            GameWorld.Famfrit, GameWorld.Hyperion, GameWorld.Lamia,
            GameWorld.Leviathan, GameWorld.Ultros
        ):
            return cls.Primal
        
        if world in (
            GameWorld.Alpha, GameWorld.Lich, GameWorld.Odin, GameWorld.Phoenix, 
            GameWorld.Raiden, GameWorld.Shiva, GameWorld.Twintania,
            GameWorld.Zodiark
        ):
            return cls.Light
        
        if world in (
            GameWorld.Cerberus, GameWorld.Louisoix, GameWorld.Moogle,
            GameWorld.Omega, GameWorld.Phantom, GameWorld.Ragnarok,
            GameWorld.Sagittarius, GameWorld.Spriggan
        ):
            return cls.Chaos

        if world in (
            GameWorld.Bismarck, GameWorld.Ravana, GameWorld.Sephirot,
            GameWorld.Sophia, GameWorld.Zurvan
        ):
            return cls.Materia

        if world in (
            GameWorld.Aegis, GameWorld.Atomos, GameWorld.Carbuncle,
            GameWorld.Garuda, GameWorld.Gungnir, GameWorld.Kujata,
            GameWorld.Tonberry, GameWorld.Typhon
        ):
            return cls.Elemental

        if world in (
            GameWorld.Alexander, GameWorld.Bahamut, GameWorld.Durandal,
            GameWorld.Fenrir, GameWorld.Ifrit, GameWorld.Ridill,
            GameWorld.Tiamat, GameWorld.Ultima
        ):
            return cls.Gaia

        if world in (
            GameWorld.Anima, GameWorld.Asura, GameWorld.Chocobo,
            GameWorld.Hades, GameWorld.Ixion, GameWorld.Masamune,
            GameWorld.Pandaemonium, GameWorld.Titan
        ):
            return cls.Mana

        if world in (
            GameWorld.Belias, GameWorld.Mandragora, GameWorld.Ramuh,
            GameWorld.Shinryu, GameWorld.Unicorn, GameWorld.Valefor,
            GameWorld.Yojimbo, GameWorld.Zeromus
        ):
            return cls.Meteor
        
        raise ValueError(f"Invalid world: {world}")
    
################################################################################
