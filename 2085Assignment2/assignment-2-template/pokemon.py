""" 
This file provides 10 classes that represent the 10 pokemon in the specifications. 

Each of these 10 pokemon inherit from the pokemon base class to share common functionality but each of them have slight variations in their stat formulas and features.
"""
from pokemon_base import PokemonBase, StatusEffect, PokeType
__author__ = "Scaffold by Jackson Goerner, Code by Jun Yu Tan, Shyam Kamalesh Borkar, Rachit Bhatia and Jobin Dan"
   
class Charmander(PokemonBase):
    """ Class for Charmander pokemon. All methods in this class have
    a best/worst case complexity of O(1).
    """
    def __init__(self) -> None:
        """ Initialise a Charmander object"""
        self.level = 1
        self.start_hp = 8 + (1 * self.level)
        PokemonBase.__init__(self, self.start_hp, PokeType.FIRE)
    
    def level_up(self) -> None:
        """ Level up Charmander"""
        self.level += 1
        new_max = 8 + (1 * self.level)
        self.hp = new_max - (self.max_hp - self.hp)
        self.max_hp = new_max
    
    def get_level(self):
        """ Get Charmander's level"""
        return self.level

    def get_speed(self) -> int:
        """ Get Charmander's speed stat"""
        speed = 7 + (1 * self.level)
        if self.status.value == "Paralysis":
            speed = speed * 0.5 # speed is halved
        speed = int (speed)
        return speed

    def get_attack_damage(self) -> int:
        """ Get Charmander's attack stat"""
        attack = 6 + (1 * self.level)
        if self.status.value == "Burn":
            attack = attack * 0.5 # attack is halved

        return attack

    def get_defence(self) -> int:
        """ Get Charmander's defence pts stat"""
        defence_pts = 4
        return defence_pts

    def defend(self, damage:int) -> int:
        """ Charmander's defend mechanism.
        :param damage: the other pokemon's effective attack
        """
        if damage > self.get_defence():
            lost_hp = damage
        else:
            lost_hp = damage // 2
        return lost_hp
    
    def get_poke_name(self) -> str:
        """ Get pokemon's name"""
        name = "Charmander"
        return name
    
    def should_evolve(self) -> bool:
        """ Indicates if the pokemon should evolve or not"""
        should_evolve = False
        if self.level >= 3:
            should_evolve = True
        return should_evolve

    def can_evolve(self) -> bool:
        """ Indicates if the pokemon is capable of evolving"""
        can_evolve = True
        return can_evolve

    def get_evolved_version(self) -> PokemonBase:
        """ Returns the evolved version of Charmander"""
        hp_difference = self.max_hp - self.hp
        charizard = Charizard()
        charizard.set_status_effect(self.get_status_effect())
        charizard.lose_hp(hp_difference)
        return charizard

class Squirtle(PokemonBase):
    """ Class for Squirtle pokemon. All methods in this class have
    a best/worst case complexity of O(1).
    """
    def __init__(self) -> None:
        """ Initialise a Squirtle object"""
        self.level = 1
        self.start_hp = 9 + (2 * self.level)
        PokemonBase.__init__(self, self.start_hp, PokeType.WATER)
    
    def level_up(self) -> None:
        """ Level up Squirtle"""
        self.level += 1
        new_max = 9 + (2 * self.level)
        self.hp = new_max - (self.max_hp - self.hp)
        self.max_hp = new_max
    
    def get_level(self):
        """ Get Squirtle's level"""
        return self.level

    def get_speed(self) -> int:
        """ Get Squirtle's speed stat"""
        speed = 7 
        if self.status.value == "Paralysis":
            speed = speed * 0.5 # speed is halved
        speed = int (speed)
        return speed

    def get_attack_damage(self) -> int:
        """ Get Squirtle's attack stat"""
        attack = 4 + (self.level // 2)
        if self.status.value == "Burn":
            attack = attack * 0.5 # attack is halved
        return attack

    def get_defence(self) -> int:
        """ Get Squirtle's defence pts stat"""
        defence_pts = 6 + self.level
        return defence_pts

    def defend(self, damage:int) -> int:       
        """ Squirtle's defend mechanism.
        :param damage: the other pokemon's effective attack
        """
        if damage > (2 * self.get_defence()):
            lost_hp = damage
        else:
            lost_hp = damage // 2
        return lost_hp
    
    def get_poke_name(self) -> str:
        """ Get pokemon's name"""
        name = "Squirtle"
        return name
    
    def should_evolve(self) -> bool:
        """ Indicates if the pokemon should evolve or not"""
        should_evolve = False
        if self.level >= 3:
            should_evolve = True
        return should_evolve

    def can_evolve(self) -> bool:
        """ Indicates if the pokemon is capable of evolving"""
        can_evolve = True
        return can_evolve

    def get_evolved_version(self) -> PokemonBase:
        """ Returns the evolved version of Squirtle"""
        hp_difference = self.max_hp - self.hp
        blastoise = Blastoise()
        blastoise.set_status_effect(self.get_status_effect())
        blastoise.lose_hp(hp_difference)
        return blastoise

class Bulbasaur(PokemonBase):
    """ Class for Bulbasaur pokemon. All methods in this class have
    a best/worst case complexity of O(1).
    """
    def __init__(self) -> None:
        """ Initialise a Bulbasaur object"""
        self.level = 1
        self.start_hp = 12 + (1 * self.level)
        PokemonBase.__init__(self, self.start_hp, PokeType.GRASS)
    
    def level_up(self) -> None:
        """ Level up Bulbasaur"""
        self.level += 1
        new_max = 12 + (1 * self.level)
        self.hp = new_max - (self.max_hp - self.hp)
        self.max_hp = new_max
    
    def get_level(self):
        """ Get Bulbasaur's level"""
        return self.level

    def get_speed(self) -> int:
        """ Get Bulbasaur's speed stat"""
        speed = 7 + (self.level // 2) 
        if self.status.value == "Paralysis":
            speed = speed * 0.5 # speed is halved
        speed = int (speed)
        return speed

    def get_attack_damage(self) -> int:
        """ Get Bulbasaur's attack stat"""
        attack = 5
        if self.status.value == "Burn":
            attack = attack * 0.5 # attack is halved
        return attack

    def get_defence(self) -> int:
        """ Get Bulbasaur's defence pts stat"""
        defence_pts = 5
        return defence_pts

    def defend(self, damage:int) -> int:
        """ Bulbasaur's defend mechanism.
        :param damage: the other pokemon's effective attack
        """
        if damage > (self.get_defence() + 5):
            lost_hp = damage
        else:
            lost_hp = damage // 2
        return lost_hp
    
    def get_poke_name(self) -> str:
        """ Get pokemon's name"""
        name = "Bulbasaur"
        return name
    
    def should_evolve(self) -> bool:
        """ Indicates if the pokemon should evolve or not"""
        should_evolve = False
        if self.level >= 2:
            should_evolve = True
        return should_evolve

    def can_evolve(self) -> bool:
        """ Indicates if the pokemon is capable of evolving"""
        can_evolve = True
        return can_evolve

    def get_evolved_version(self) -> PokemonBase:
        """ Returns the evolved version of Bulbasaur"""
        hp_difference = self.max_hp - self.hp
        venusaur = Venusaur()
        venusaur.set_status_effect(self.get_status_effect())
        venusaur.lose_hp(hp_difference)
        return venusaur

class Gastly(PokemonBase):
    """ Class for Gastly pokemon. All methods in this class have
    a best/worst case complexity of O(1).
    """
    def __init__(self) -> None:
        """ Initialise a Gastly object"""
        self.level = 1
        self.start_hp = 6 + (self.level // 2)
        PokemonBase.__init__(self, self.start_hp, PokeType.GHOST)
    
    def level_up(self) -> None:
        """ Level up Gastly"""
        self.level += 1
        new_max = 6 + (self.level // 2)
        self.hp = new_max - (self.max_hp - self.hp)
        self.max_hp = new_max
    
    def get_level(self):
        """ Get Gastly's level"""
        return self.level

    def get_speed(self) -> int:
        """ Get Gastly's speed stat"""
        speed = 2
        if self.status.value == "Paralysis":
            speed = speed * 0.5 # speed is halved
        speed = int (speed)
        return speed

    def get_attack_damage(self) -> int:
        """ Get Gastly's attack stat"""
        attack = 4
        if self.status.value == "Burn":
            attack = attack * 0.5 # attack is halved
        return attack

    def get_defence(self) -> int:
        """ Get Gastly's defence pts stat"""
        defence_pts = 8
        return defence_pts

    def defend(self, damage:int) -> int:
        """ Gastly's defend mechanism.
        :param damage: the other pokemon's effective attack
        """
        lost_hp = damage
        return lost_hp
    
    def get_poke_name(self) -> str:
        """ Get pokemon's name"""
        name = "Gastly"
        return name
    
    def should_evolve(self) -> bool:
        """ Indicates if the pokemon should evolve or not"""
        should_evolve = False
        if self.level >= 1:
            should_evolve = True
        return should_evolve

    def can_evolve(self) -> bool:
        """ Indicates if the pokemon is capable of evolving"""
        can_evolve = True
        return can_evolve

    def get_evolved_version(self) -> PokemonBase:
        """ Returns the evolved version of Gastly"""
        hp_difference = self.max_hp - self.hp
        haunter = Haunter()
        haunter.set_status_effect(self.get_status_effect())
        haunter.lose_hp(hp_difference)
        # Hauter should have the same level as gastly. as they both start from level 1
        for i in range(self.get_level() - 1):
            haunter.level_up()
            
        return haunter

class Eevee(PokemonBase):
    """ Class for Eevee pokemon. All methods in this class have
    a best/worst case complexity of O(1).
    """
    def __init__(self) -> None:
        """ Initialise a Eevee object"""
        self.level = 1
        self.start_hp = 10
        PokemonBase.__init__(self, self.start_hp, PokeType.NORMAL)
    
    def level_up(self) -> None:
        """ Level up Eevee"""
        self.level += 1
        new_max = 10
        self.hp = new_max - (self.max_hp - self.hp)
        self.max_hp = new_max
    
    def get_level(self):
        """ Get Eevee's level"""
        return self.level

    def get_speed(self) -> int:
        """ Get Eevee's speed stat"""
        speed = 7 + self.level
        if self.status.value == "Paralysis":
            speed = speed * 0.5 # speed is halved
        speed = int (speed)
        return speed

    def get_attack_damage(self) -> int:
        """ Get Eevee's attack stat"""
        attack = 6 + self.level
        if self.status.value == "Burn":
            attack = attack * 0.5 # attack is halved
        return attack

    def get_defence(self) -> int:
        """ Get Eevee's defence pts stat"""
        defence_pts = 4 + self.level
        return defence_pts

    def defend(self, damage:int) -> int:
        """ Eevee's defend mechanism.
        :param damage: the other pokemon's effective attack
        """
        if damage >= self.get_defence():
            lost_hp = damage
        else:
            lost_hp = 0
        return lost_hp
    
    def get_poke_name(self) -> str:
        """ Get pokemon's name"""
        name = "Eevee"
        return name
    
    def should_evolve(self) -> bool:
        """ Indicates if the pokemon should evolve or not"""
        should_evolve = False
        return should_evolve

    def can_evolve(self) -> bool:
        """ Indicates if the pokemon is capable of evolving"""
        can_evolve = False
        return can_evolve

    def get_evolved_version(self) -> PokemonBase:
        """ Returns the evolved version of Eevee"""
        return self

class Charizard(PokemonBase):
    """ Class for Charizard pokemon. All methods in this class have
    a best/worst case complexity of O(1).
    """
    def __init__(self) -> None:
        """ Initialise a Charizard object"""
        self.level = 3
        self.start_hp = 12 + (1 * self.level)
        PokemonBase.__init__(self, self.start_hp, PokeType.FIRE)
    
    def level_up(self) -> None:
        """ Level up Charizard"""
        self.level += 1
        new_max = 12 + (1 * self.level)
        self.hp = new_max - (self.max_hp -self.hp)
        self.max_hp = new_max
    
    def get_level(self):
        """ Get Charizard's level"""
        return self.level

    def get_speed(self) -> int:
        """ Get Charizard's speed stat"""
        speed = 9 + (1 * self.level)
        if self.status.value == "Paralysis":
            speed = speed * 0.5 # speed is halved
        speed = int (speed)
        return speed

    def get_attack_damage(self) -> int:
        """ Get Charizard's attack stat"""
        attack = 10 + (2 * self.level)
        if self.status.value == "Burn":
            attack = attack * 0.5 # attack is halved
        return attack

    def get_defence(self) -> int:
        """ Get Charizard's defence pts stat"""
        defence_pts = 4
        return defence_pts

    def defend(self, damage:int) -> int:
        """ Charizard's defend mechanism.
        :param damage: the other pokemon's effective attack
        """
        if damage > self.get_defence():
            lost_hp = 2 * damage
        else:
            lost_hp = damage
        return lost_hp
    
    def get_poke_name(self) -> str:
        """ Get pokemon's name"""
        name = "Charizard"
        return name
    
    def should_evolve(self) -> bool:
        """ Indicates if the pokemon should evolve or not"""
        should_evolve = False
        return should_evolve

    def can_evolve(self) -> bool:
        """ Indicates if the pokemon is capable of evolving"""
        can_evolve = False
        return can_evolve

    def get_evolved_version(self) -> PokemonBase:
        """ Returns the evolved version of Charizard"""
        return self

class Blastoise(PokemonBase):
    """ Class for Blastoise pokemon. All methods in this class have
    a best/worst case complexity of O(1).
    """
    def __init__(self) -> None:
        """ Initialise a Blastoise object"""
        self.level = 3
        self.start_hp = 15 + (2 * self.level)
        PokemonBase.__init__(self, self.start_hp, PokeType.WATER)
    
    def level_up(self) -> None:
        """ Level up Blastoise"""
        self.level += 1
        new_max = 15 + (2 * self.level)
        self.hp = new_max - (self.max_hp -self.hp)
        self.max_hp = new_max
    
    def get_level(self):
        """ Get Blastoise's level"""
        return self.level

    def get_speed(self) -> int:
        """ Get Blastoise's speed stat"""
        speed = 10
        if self.status.value == "Paralysis":
            speed = speed * 0.5 # speed is halved
        speed = int (speed)
        return speed

    def get_attack_damage(self) -> int:
        """ Get Blastoise's attack stat"""
        attack = 8 + (self.level // 2)
        if self.status.value == "Burn":
            attack = attack * 0.5 # attack is halved
        return attack

    def get_defence(self) -> int:
        """ Get Blastoise's defence pts stat"""
        defence_pts = 8 + (1 * self.level)
        return defence_pts

    def defend(self, damage:int) -> int:
        """ Blastoise's defend mechanism.
        :param damage: the other pokemon's effective attack
        """
        if damage > (2 * self.get_defence()):
            lost_hp = damage
        else:
            lost_hp = damage // 2
        return lost_hp
    
    def get_poke_name(self) -> str:
        """ Get pokemon's name"""
        name = "Blastoise"
        return name
    
    def should_evolve(self) -> bool:
        """ Indicates if the pokemon should evolve or not"""
        should_evolve = False
        return should_evolve

    def can_evolve(self) -> bool:
        """ Indicates if the pokemon is capable of evolving"""
        can_evolve = False
        return can_evolve

    def get_evolved_version(self) -> PokemonBase:
        """ Returns the evolved version of Blastoise"""
        return self

class Venusaur(PokemonBase):
    """ Class for Venusaur pokemon. All methods in this class have
    a best/worst case complexity of O(1).
    """
    def __init__(self) -> None:
        """ Initialise a Venusaur object"""
        self.level = 2
        self.start_hp = 20 + (self.level // 2)
        PokemonBase.__init__(self, self.start_hp, PokeType.GRASS)
    
    def level_up(self) -> None:
        """ Level up Venusaur"""
        self.level += 1
        new_max = 20 + (self.level // 2)
        self.hp = new_max - (self.max_hp -self.hp)
        self.max_hp = new_max
    
    def get_level(self):
        """ Get Venusaur's level"""
        return self.level

    def get_speed(self) -> int:
        """ Get Venusaur's speed stat"""
        speed = 3 + (self.level // 2)
        if self.status.value == "Paralysis":
            speed = speed * 0.5 # speed is halved
        speed = int (speed)
        return speed

    def get_attack_damage(self) -> int:
        """ Get Venusaur's attack stat"""
        attack = 5
        if self.status.value == "Burn":
            attack = attack * 0.5 # attack is halved
        return attack

    def get_defence(self) -> int:
        """ Get Venusaur's defence pts stat"""
        defence_pts = 10
        return defence_pts

    def defend(self, damage:int) -> int:
        """ Venusaur's defend mechanism.
        :param damage: the other pokemon's effective attack
        """
        if damage > (self.get_defence() + 5):
            lost_hp = damage
        else:
            lost_hp = damage // 2
        return lost_hp
    
    def get_poke_name(self) -> str:
        """ Get pokemon's name"""
        name = "Venusaur"
        return name
    
    def should_evolve(self) -> bool:
        """ Indicates if the pokemon should evolve or not"""
        should_evolve = False
        return should_evolve

    def can_evolve(self) -> bool:
        """ Indicates if the pokemon is capable of evolving"""
        can_evolve = False
        return can_evolve

    def get_evolved_version(self) -> PokemonBase:
        """ Returns the evolved version of Venusaur"""
        return self

class Haunter(PokemonBase):
    """ Class for Haunter pokemon. All methods in this class have
    a best/worst case complexity of O(1).
    """
    def __init__(self) -> None:
        """ Initialise a Haunter object"""
        self.level = 1
        self.start_hp = 9 + (self.level // 2)
        PokemonBase.__init__(self, self.start_hp, PokeType.GHOST)
    
    def level_up(self) -> None:
        """ Level up Haunter"""
        self.level += 1
        new_max = 9 + (self.level // 2)
        self.hp = new_max - (self.max_hp -self.hp)
        self.max_hp = new_max
    
    def get_level(self):
        """ Get Haunter's level"""
        return self.level

    def get_speed(self) -> int:
        """ Get Haunter's speed stat"""
        speed = 6
        if self.status.value == "Paralysis":
            speed = speed * 0.5 # speed is halved
        speed = int (speed)
        return speed

    def get_attack_damage(self) -> int:
        """ Get Haunter's attack stat"""
        attack = 8
        if self.status.value == "Burn":
            attack = attack * 0.5 # attack is halved
        return attack

    def get_defence(self) -> int:
        """ Get Haunter's defence pts stat"""
        defence_pts = 6
        return defence_pts

    def defend(self, damage:int) -> int:
        """ Haunter's defend mechanism.
        :param damage: the other pokemon's effective attack
        """
        lost_hp = damage 
        return lost_hp
    
    def get_poke_name(self) -> str:
        """ Get pokemon's name"""
        name = "Haunter"
        return name
    
    def should_evolve(self) -> bool:
        """ Indicates if the pokemon should evolve or not"""
        should_evolve = False
        if self.level >= 3:
            should_evolve = True
        return should_evolve

    def can_evolve(self) -> bool:
        """ Indicates if the pokemon is capable of evolving"""
        can_evolve = True
        return can_evolve

    def get_evolved_version(self) -> PokemonBase:
        """ Returns the evolved version of Haunter"""
        hp_difference = self.max_hp - self.hp
        gengar = Gengar()
        gengar.set_status_effect(self.get_status_effect())
        gengar.lose_hp(hp_difference)
        return gengar

class Gengar(PokemonBase):
    """ Class for Gengar pokemon. All methods in this class have
    a best/worst case complexity of O(1).
    """
    def __init__(self) -> None:
        """ Initialise a Gengar object"""
        self.level = 3
        self.start_hp = 12 + (self.level // 2)
        PokemonBase.__init__(self, self.start_hp, PokeType.GHOST)
    
    def level_up(self) -> None:
        """ Level up Gengar"""
        self.level += 1
        new_max = 12 + (self.level // 2)
        self.hp = new_max - (self.max_hp -self.hp)
        self.max_hp = new_max
    
    def get_level(self):
        """ Get Gengar's level"""
        return self.level

    def get_speed(self) -> int:
        """ Get Gengar's speed stat"""
        speed = 12
        if self.status.value == "Paralysis":
            speed = speed * 0.5 # speed is halved
        speed = int (speed)
        return speed

    def get_attack_damage(self) -> int:
        """ Get Gengar's attack stat"""
        attack = 18
        if self.status.value == "Burn":
            attack = attack * 0.5 # attack is halved
        return attack

    def get_defence(self) -> int:
        """ Get Gengar's defence pts stat"""
        defence_pts = 3
        return defence_pts

    def defend(self, damage:int) -> int:
        """ Gengar's defend mechanism.
        :param damage: the other pokemon's effective attack
        """
        lost_hp = damage 
        return lost_hp
    
    def get_poke_name(self) -> str:
        """ Get pokemon's name"""
        name = "Gengar"
        return name
    
    def should_evolve(self) -> bool:
        """ Indicates if the pokemon should evolve or not"""
        should_evolve = False
        return should_evolve

    def can_evolve(self) -> bool:
        """ Indicates if the pokemon is capable of evolving"""
        can_evolve = False
        return can_evolve

    def get_evolved_version(self) -> PokemonBase:
        """ Returns the evolved version of Gengar"""
        return self


