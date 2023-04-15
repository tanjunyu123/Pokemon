from __future__ import annotations


""" This file contains a Poketeam class that will allow the creation of pokemon teams with a 
certain number of pokemons. Teams can have different features like battle mode, ai mode and criterion
for a particular battle mode.
"""
__author__ = "Scaffold by Jackson Goerner, Code by Jun Yu Tan and Shyam Kamalesh Borkar."


from enum import Enum, auto
from pokemon_base import PokemonBase
from pokemon import *
from random_gen import RandomGen
from array_sorted_list import ArraySortedList
from queue_adt import CircularQueue
from stack_adt import  ArrayStack
from sorted_list import ListItem
from pokemon_base import StatusEffect


class Action(Enum):
    """ Enumumeration class Action to symbolise different actions that can be done"""
    ATTACK = auto()
    SWAP = auto()
    HEAL = auto()
    SPECIAL = auto()

class Criterion(Enum):
    """ Enumumeration class Criterion to symbolise different sorting criteria"""
    SPD = auto()
    HP = auto()
    LV = auto()
    DEF = auto()

class PokeTeam:
    """ Poketeam class to manage pokemons and featues of the poke team"""

    class AI(Enum):
        """ Enumumeration class AI to symbolise different AI modes available"""
        ALWAYS_ATTACK = auto()
        SWAP_ON_SUPER_EFFECTIVE = auto()
        RANDOM = auto()
        USER_INPUT = auto()

    def __init__(self, team_name: str, team_numbers: list[int], battle_mode: int, ai_type: PokeTeam.AI, criterion=None, criterion_value=None) -> None:
        """ Initialises the pokemon team object with its attributes
        :param team_name: the name of the pokemon team
        :param team_numbers: the list of integers representing the pokemons in the team
        :param battle_mode: the battle mode of the team
        :param ai_type: the AI mode that the team will follow
        :param criterion: the criteria in which team in battle mode 2 is sorted
        :pre: team_name must be a string
        :pre: battle_mode must be an integer
        :pre: battle_mode can only be one of 1, 2 and 3
        :pre: battle_mode 2 must have a specified criterion with it
        :raises TypeError: if team_name is not a string
        :raises TypeError: if battle_mode is not an integer
        :raises ValueError: if battle_mode is not 1, 2 or 3
        :raises Exception: if criterion is not specified for battle_mode 2

        :complexity: Best and worst case complexity is O(S) where S is the complexity
        of set_team()
        """

        if not type(team_name) == str:
            raise TypeError("A string is expected for Team Name.")
        if not type(battle_mode) == int:
            raise TypeError("An integer is expected for Battle Mode.")
        if not (battle_mode == 0 or battle_mode == 1 or battle_mode == 2):
            raise ValueError("Invalid Battle Mode.")
        if battle_mode == 2 and criterion == None :
            raise Exception("Criterion is not specified for Battle Mode 2")
        # Check if the number of pokemons exceeds 6
        sum = 0
        for num in team_numbers:
            sum += num
        if sum > 6:
            raise ValueError("Number of pokemons exceeds team limit")

        self.num_of_pokemons = sum

        self.team_name = team_name
        self.team_numbers = team_numbers
        self.battle_mode = battle_mode
        self.ai_type = ai_type

        self.criterion = criterion
        # team will be the data type according to battle mode
        self.team = None

        self.set_team()


        self.num_of_heals = 3

    @classmethod
    def random_team(cls, team_name: str, battle_mode: int, team_size=None, ai_mode=None, criterion = None)-> PokeTeam:
        """ class method that creates random poke team following some steps
        :param team_name: the name of the pokemon team
        :param team_numbers: the list of integers representing the pokemons in the team
        :param battle_mode: the battle mode of the team
        :param ai_type: the AI mode that the team will follow
        :param criterion: the criteria in which team in battle mode 2 is sorted

        :complexity: Best and worst case is O(n + P) where n is the lenght of random_team_numbers and
                     P is the complexity of creating a poketeam.
        """

        if team_size == None:
            team_size = RandomGen.randint(3, 6)

        random_team_numbers = ArraySortedList(6)
        random_team_numbers.add(ListItem(None,0))
        random_team_numbers.add(ListItem(None, team_size))

        first_random = RandomGen.randint(0, team_size)
        second_random = RandomGen.randint(0, team_size)
        third_random = RandomGen.randint(0, team_size)
        fourth_random = RandomGen.randint(0, team_size)

        random_team_numbers.add(ListItem(None,first_random))
        random_team_numbers.add(ListItem(None,second_random))
        random_team_numbers.add(ListItem(None,third_random))
        random_team_numbers.add(ListItem(None,fourth_random))

        # array that stores the number of each pokemon
        team_numbers = []
        for i in range(0, len(random_team_numbers) - 1):
            team_numbers.append(random_team_numbers[i+1].key - random_team_numbers[i].key)

        if ai_mode is None:
            ai_mode = PokeTeam.AI.RANDOM

        random_team = PokeTeam(team_name,team_numbers,battle_mode,ai_mode, criterion = criterion)

        return random_team

    def return_pokemon(self, pokemon: PokemonBase) -> None:
        """ returns a pokemon back into the team according to the team's battle mode
        :param pokemon: the pokemon to be returned back to the team
        :complexity: Best case complexity is O(1) for battle mode 0 and 1 (Stack and Cricular Queue).
        Worst case complexity is O(n) where n is the current lenght of the Array Sorted List (for battle mode 2).
        """

        if not pokemon.is_fainted():
            pokemon.set_status_effect(StatusEffect.NONE)

            if self.battle_mode == 0: # ArrayStack
                self.team.push(pokemon)
            elif self.battle_mode == 1: # CircularQueue
                self.team.append(pokemon)
            elif self.battle_mode == 2: # ArraySortedList
                if self.criterion == Criterion.SPD:
                    self.team.add(ListItem(pokemon, pokemon.get_speed()))
                elif self.criterion == Criterion.HP:
                    self.team.add(ListItem(pokemon, pokemon.get_hp()))
                elif self.criterion == Criterion.LV:
                    self.team.add(ListItem(pokemon, pokemon.get_level()))
                elif self.criterion == Criterion.DEF:
                    self.team.add(ListItem(pokemon, pokemon.get_defence()))
            
    def retrieve_pokemon(self) -> PokemonBase | None:
        """ retrieves a pokemon from the team according to the team's battle mode
        :complexity: Best case complexity of O(1) for battle mode 0 and 1.
        Worst case complexity of O(m) where m is the length of the array
        sorted list after removing the first element.
        """
        if self.is_empty():
            pokemon = None
        elif self.battle_mode == 0:  # ArrayStack
            pokemon = self.team.pop()
        elif self.battle_mode == 1:  # CircularQueue
            pokemon = self.team.serve()
        elif self.battle_mode == 2:  # ArraySortedList
            pokemon = self.team.delete_at_index(0).value
        
        return pokemon

    def special(self) -> None:
        """ carries out a special operation on the pokemon team based on the battle mode
        :complexity: Battle Mode 0 - Best and worst is O(n) where n is the length of the stack
                     Battle Mode 1 - Best and worst is O(n) where n is the length of the queue
                     Battle Mode 2 - Best is O(1) when the list is already sorted or the first iteration produces sorting result (Bubble sort)
                                     Worst is O(n^2) where n is the length of the list (Bubble sort)
        """
        if self.battle_mode == 0:  # ArrayStack
            # Swap the first and last pokemon in the stack if the stack'sl lenth is greater than 1
            if len(self.team) > 1:

                temp_stack = ArrayStack(len(self.team) - 2)

                first_pokemon = self.team.pop()

                while len(self.team) > 1:
                    temp_stack.push(self.team.pop())
                
                last_pokemon = self.team.pop()

                self.team.push(first_pokemon)

                while len(temp_stack) > 0:
                    self.team.push(temp_stack.pop())
                
                self.team.push(last_pokemon)


        if self.battle_mode == 1:  # CircularQueue
            # swap the first and second halves of the CircularQueue
            half_number = len(self.team) // 2
            temp_stack = ArrayStack(half_number)

            for _ in range(half_number):
                temp_stack.push(self.team.serve())
            
            for _ in range(half_number):
                self.team.append(temp_stack.pop())


        if self.battle_mode == 2:  # ArraySortedList
            self.team.reverse_order()


    def regenerate_team(self) -> None:        
        """ regenerates the team by building the team back from the team numbers
        :complexity: Best and worst case complexity is O(S) where S is the complexity
        of set_team()
        """
        self.set_team()
        self.num_of_heals = 3

    def __str__(self) -> str:
        """ magic method that produces the string version of the pokemon team
        :complexity: Battle Mode 0 - Best and worst is O(n) where n is the length of the stack
                     Battle Mode 1 - Best and worst is O(n) where n is the length of the queue
                     Battle Mode 2 - Best and worst is O(n) where n is the length of the array sorted list
        """
        result = self.team_name + " " + "(" + str(self.battle_mode) + ")" + ": "

        pokemon_str_list = ""

        if self.battle_mode == 0:  # ArrayStack
            stack_length = len(self.team)
            for _ in range(stack_length):
                pokemon_str_list += str(self.team.peek()) + ", "
                self.team.length -= 1
            self.team.length = stack_length
                
        elif self.battle_mode == 1:  # CircularQueue
            for _ in range(len(self.team)):
                pokemon = self.team.serve()
                pokemon_str_list += str(pokemon) + ", "
                self.team.append(pokemon)

        elif self.battle_mode == 2:  # ArraySortedList
            for i in range(len(self.team)):
                pokemon = self.team[i].value
                pokemon_str_list += str(pokemon) + ", "

        result += "[" + pokemon_str_list[0:-2] + "]"
        return result

    def is_empty(self):
        """ returns if the pokemon team is empty or not
        :complexity: Best and worst case complexity is O(1)
        """
        is_empty = len(self.team) == 0
        return is_empty


    def choose_battle_option(self, my_pokemon: PokemonBase, their_pokemon: PokemonBase) -> Action:
        """ Chooses the action that a pokemon will do based on the AI mode
        :param my_pokemon: the pokemon that will do the action from this team
        :param their_pokemon: the other teams pokemon
        :complexity: Best and worst case complexity is O(1)
        """
        if self.ai_type == PokeTeam.AI.ALWAYS_ATTACK:
            action = Action.ATTACK
        elif self.ai_type == PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE: 
            if their_pokemon.get_attack_damage() * their_pokemon.get_effective_multiplier(my_pokemon) >= 1.5 * their_pokemon.get_attack_damage():
                action = Action.SWAP
            else:
                action = Action.ATTACK
        elif self.ai_type == PokeTeam.AI.RANDOM:
            actions = list(Action)
            # remove the heal action if team has used their max heals
            if self.num_of_heals <= 0:
                actions.remove(Action.HEAL)

            action = actions[RandomGen.randint(0, len(actions) - 1)]

        elif self.ai_type == PokeTeam.AI.USER_INPUT:
            print("Available Actions:")
            print("(1) Attack")
            print("(2) Swap")
            print("(3) Heal")
            print("(4) Special")
            choice = int(input("Enter Option: "))
            action = Action(choice)

        return action

    def set_team(self) -> None:
        """ Set up the pokemon team by calling the appopriate fill team modes for the 3 battle modes
        :complexity: Battle Mode 0 - Best and worst is O(f0) where f0 is the complexity of fill_team_mode_zero()
                     Battle Mode 1 - Best and worst is O(f1) where f1 is the complexity of fill_team_mode_one()
                     Battle Mode 2 - Best case complexity is O(f2) where f2 is the complexity of fill_team_mode_two()
                                     Worst case complexity is O(f2 + n^2) where f2 is the complexity of fill_team_mode_two() and
                                     n is the length of the array sorted list for battle mode 2
        """
        if self.battle_mode == 0: # ArrayStack
            self.team = ArrayStack(self.num_of_pokemons)
            self.fill_team_mode_zero()
        elif self.battle_mode == 1: # CircularQueue
            self.team = CircularQueue(self.num_of_pokemons)
            self.fill_team_mode_one()
        elif self.battle_mode == 2: # ArraySortedList
            self.team = ArraySortedList(self.num_of_pokemons)
            self.fill_team_mode_two()
            self.team.reverse_order()

    def fill_team_mode_zero(self) -> None:
        """ fills up the pokemon team according to battle mode zero
        :complexity: Best and worst case complexity is O(n*m) where n is the length of the team/stack and
        m is the length of the team numbers
        """

        for i in range(len(self.team_numbers)-1,-1,-1):

            for j in range(self.team_numbers[i]):
                
                if i == 0:
                    pokemon = Charmander()
                elif i == 1:
                    pokemon = Bulbasaur()
                elif i == 2:
                    pokemon = Squirtle()
                elif i == 3:
                    pokemon = Gastly()
                elif i == 4:
                    pokemon = Eevee()
                self.team.push(pokemon)

    def fill_team_mode_one(self) -> None:
        """ fills up the pokemon team according to battle mode one
        :complexity: Best and worst case complexity is O(n*m) where n is the length of the team/queue and
        m is the length of the team numbers
        """

        for i in range(len(self.team_numbers)):

            for j in range(self.team_numbers[i]):
                if i == 0:
                    pokemon = Charmander()
                elif i == 1:
                    pokemon = Bulbasaur()
                elif i == 2:
                    pokemon = Squirtle()
                elif i == 3:
                    pokemon = Gastly()
                elif i == 4:
                    pokemon = Eevee()
                self.team.append(pokemon)

    def fill_team_mode_two(self) -> None:
        """ fills up the pokemon team according to battle mode two
        :complexity: Best and worst case complexity is O(n*m) where n is the length of the team/sorted list and
        m is the length of the team numbers
        """
        
        for i in range(len(self.team_numbers)):

            for j in range(self.team_numbers[i]):
                if i == 0:
                    pokemon = Charmander()
                elif i == 1:
                    pokemon = Bulbasaur()
                elif i == 2:
                    pokemon = Squirtle()
                elif i == 3:
                    pokemon = Gastly()
                elif i == 4:
                    pokemon = Eevee()
                    
                if self.criterion == Criterion.SPD:
                    self.team.add(ListItem(pokemon, pokemon.get_speed()))
                elif self.criterion == Criterion.HP:
                    self.team.add(ListItem(pokemon, pokemon.get_hp()))
                elif self.criterion == Criterion.LV:
                    self.team.add(ListItem(pokemon, pokemon.get_level()))
                elif self.criterion == Criterion.DEF:
                    self.team.add(ListItem(pokemon, pokemon.get_defence()))
    
    def get_team_numbers(self) -> list[int]:
        """ return the team numbers (list)
        :complexity: Best and worst case complexity is O(1)
        """
        return self.team_numbers

    @classmethod
    def leaderboard_team(cls):
        raise NotImplementedError()
