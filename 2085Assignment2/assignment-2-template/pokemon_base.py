from __future__ import annotations
from abc import ABC, abstractmethod 
from typing import TypeVar, Generic 
from enum import Enum
from random_gen import RandomGen

__author__ = "Scaffold by Jackson Goerner, Code by Jun Yu Tan, Shyam Kamalesh Borkar, Rachit Bhatia and Jobin Dan"

""" Enumumeration class PokeType to symbolises the Pokemon Types"""

class PokeType(Enum):
    FIRE = "Fire"
    GRASS = "Grass"
    WATER = "Water"
    GHOST = "Ghost"
    NORMAL = "Normal"

""" Enumumeration class Satus to symbolise names for Pokemon Types"""

class StatusEffect(Enum):
    NONE = "None"
    BURN = "Burn"
    POISON = "Poison"
    PARALYSIS = "Paralysis"
    SLEEP = "Sleep"
    CONFUSTION = "Confusion"


T = TypeVar('T')

""" An abstract class that abstracts all the functionality of a pokemon. Each pokemon can 
inherit this class to avoid repetition of functionality.
"""

class PokemonBase(ABC, Generic[T]):

    def __init__(self, hp: int, poke_type: PokeType) -> None:
        """ Initialises the pokemon object with its attributes
        :param hp: the starting hp of the pokemon
        :param poke_type: the type of the pokemon
        :pre: hp must be greater than zero
        :raises ValueError: if hp not greater than zero
        :complexity: Best and worst case complexity is O(1)
        """
        if hp <= 0:
            raise ValueError("Max hp must be greater than zero!")
        self.hp = hp
        self.poke_type = poke_type
        self.status = StatusEffect.NONE
        self.max_hp = self.hp

    def is_fainted(self) -> bool:
        """ checks if the pokemon is fainted by checking if hp is less than
        or equal to zero

        :complexity: Best and worst case complexity is O(1)
        """
        if self.hp <= 0:
            return True
        else:
            return False
    
    def get_hp(self):
        """ returns the hp of the pokemon
        :complexity: Best and worst case complexity is O(1)
        """
        return self.hp
    
    def heal(self):
        """ heals the pokemon by making hp maximum and removing status effects
        :complexity: Best and worst case complexity is O(1)
        """
        self.hp = self.max_hp
        self.status = StatusEffect.NONE

    @abstractmethod
    def get_level(self):
        """ returns the level of the pokemon"""
        pass
    
    @abstractmethod
    def level_up(self) -> None:
        """ levels the pokemon up by one"""
        pass

    @abstractmethod
    def get_speed(self) -> int:
        """ returns the speed of the pokemon"""
        pass

    @abstractmethod
    def get_attack_damage(self) -> int:
        """ returns the attack points of the pokemon"""
        pass

    @abstractmethod
    def get_defence(self) -> int:
        """ returns the level of the pokemon"""
        pass

    def lose_hp(self, lost_hp: int) -> None:
        """ Deducts health points from the pokemon
        :param lost_hp: the health points value that the pokemon must lose
        :complexity: Best and worst case complexity is O(1)
        """
        self.hp -= lost_hp

    @abstractmethod
    def defend(self, damage: int) -> None:
        """ Carries out the defense mechanism of the pokemon
        :param damage: the damage that opponent pokemon can inflict
        """
        pass      

    def attack(self, other: PokemonBase):
        """ conducts an attack between two pokemon

        :param other: the opponent pokemon that will be attacked
        :complexity: Best and worst case complexity is O(1)
        """
        # Step 1: Status effects on attack damage / redirecting attacks
        # Step 2: Do the attack
        # Step 3: Losing hp to status effects
        # Step 4: Possibly applying status effects

        if self.status.value == "Sleep":
            return 
    
        if self.status.value == "Confusion" and RandomGen.random_chance(0.5):
            other = self

        effective_attack = self.get_attack_damage() * self.get_effective_multiplier(other)
        effective_attack =  int (effective_attack)
        defence_calculation = other.defend(effective_attack)
        other.lose_hp(defence_calculation)

        if self.status.value == "Burn":
            self.lose_hp(1)
        elif self.status.value == "Poison":
            self.lose_hp(3)

        if RandomGen.random_chance(0.2):
            other.status = self.get_inflict_status()
                

    @abstractmethod
    def get_poke_name(self) -> str:
        """ returns the name of the pokemon itself"""
        pass

    def __str__(self) -> str:
        """ returns the string form of the pokemon conveying information such 
        as the pokemon name, level and health points
        :complexity: Best and worst case complexity is O(1)
        """
        pokemon_string = "LV. " + str(self.get_level()) + " " + self.get_poke_name() + ": " + str(self.hp) + " HP"
        return pokemon_string

    @abstractmethod
    def should_evolve(self) -> bool:
        """returns a boolean that validates if the pokemon should evolve or not"""
        pass

    @abstractmethod
    def can_evolve(self) -> bool:
        """returns a boolean that validates if the pokemon should evolve or not"""
        pass

    @abstractmethod
    def get_evolved_version(self) -> PokemonBase:
        """returns boolean that validates if the pokemon should eveolve or not"""
        pass

    def get_effective_multiplier(self, other: PokemonBase) -> float:

        """ returns the appropriate attack multiplier based on the pokemon's type and 
        the opponent pokemon's type.

        :param other: the other opponent pokemon
        :complexity: Best and worst case complexity is O(1)
        """

        multiplier = 1 #setting default to 1

        if self.poke_type.value == "Fire":
            if other.poke_type.value == "Fire":
                multiplier = 1
            elif other.poke_type.value == "Grass":
                multiplier = 2
            elif other.poke_type.value == "Water":
                multiplier = 0.5
            elif other.poke_type.value == "Ghost":
                multiplier = 1
            elif other.poke_type.value == "Normal":
                multiplier = 1
    
        elif self.poke_type.value == "Grass":
            if other.poke_type.value == "Fire":
                multiplier = 0.5
            elif other.poke_type.value == "Grass":
                multiplier = 1
            elif other.poke_type.value == "Water":
                multiplier = 2
            elif other.poke_type.value == "Ghost":
                multiplier = 1
            elif other.poke_type.value == "Normal":
                multiplier = 1

        elif self.poke_type.value == "Water":
            if other.poke_type.value == "Fire":
                multiplier = 2
            elif other.poke_type.value == "Grass":
                multiplier = 0.5
            elif other.poke_type.value == "Water":
                multiplier = 1
            elif other.poke_type.value == "Ghost":
                multiplier = 1
            elif other.poke_type.value == "Normal":
                multiplier = 1

        elif self.poke_type.value == "Ghost":
            if other.poke_type.value == "Fire":
                multiplier = 1.25
            elif other.poke_type.value == "Grass":
                multiplier = 1.25
            elif other.poke_type.value == "Water":
                multiplier = 1.25
            elif other.poke_type.value == "Ghost":
                multiplier = 2
            elif other.poke_type.value == "Normal":
                multiplier = 0

        elif self.poke_type.value == "Normal":
            if other.poke_type.value == "Fire":
                multiplier = 1.25
            elif other.poke_type.value == "Grass":
                multiplier = 1.25
            elif other.poke_type.value == "Water":
                multiplier = 1.25
            elif other.poke_type.value == "Ghost":
                multiplier = 0
            elif other.poke_type.value == "Normal":
                multiplier = 1

        return multiplier


    def get_inflict_status(self) -> StatusEffect:

        """ returns the appropriate status effect that the pokemon inflicts on an
        opponent based on its own pokemon type.

        :complexity: Best and worst case complexity is O(1)
        """

        new_status = StatusEffect.NONE

        if self.poke_type.value == "Fire":
            new_status = StatusEffect.BURN
        elif self.poke_type.value == "Grass":
            new_status = StatusEffect.POISON
        elif self.poke_type.value == "Water":
            new_status = StatusEffect.PARALYSIS
        elif self.poke_type.value == "Ghost":
            new_status = StatusEffect.SLEEP
        elif self.poke_type.value == "Normal":
            new_status = StatusEffect.CONFUSTION
        
        return new_status

    def get_status_effect(self) -> StatusEffect:
        """ returns the pokemon's status
        :complexity: Best and worst case complexity is O(1)
        """
        return self.status

    def set_status_effect(self, new_status_effect: StatusEffect):
        """ sets the pokemon's status
        :complexity: Best and worst case complexity is O(1)
        """
        self.status = new_status_effect
