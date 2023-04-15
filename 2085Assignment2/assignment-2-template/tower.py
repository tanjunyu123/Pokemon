from __future__ import annotations
from typing import Tuple

from poke_team import PokeTeam
from battle import Battle
from queue_adt import CircularQueue
from random_gen import RandomGen

__author__ = "Scaffold by Jackson Goerner and code by Shyam Kamalesh Borkar"

""" Class for creating a Battle Tower.

This class sets up a team and a tower of teams which the team will have fight 
through. If the team loses even one battle with the team in the tower, the 
tower ends. If the team wins all battles and the remaining lives of all the teams
are 0 the team is victorious.
"""
class BattleTower:

    """ Class to setup a Battle Tower for the team to fight through"""

    def __init__(self, battle: Battle|None=None) -> None:
        """ Sets up tha battle between the player's team and the tower.

        :param battle: the battle setup that will be used for the team and the tower.
        :complexity: Best and worst case complexity is O(1)
        """
        self.battle = battle
        self.fighting_team = None
        self.teams = None
        self.teams_lives = None

    def set_my_team(self, team: PokeTeam) -> None:
        """ Sets the team that is going to battle through the tower.

        :param team: the Poke Team that is going to battle through the tower
        :complexity: Best and worst case complexity is O(1)
        """
        self.fighting_team = team

    def generate_teams(self, n: int) -> None:
        """ Generates teams for the Battle tower.

        :param n: the number of teams to be generated for the tower.
        :raises TypeError: if n is not an integer
        :raises ValueError: if n is not greater than 0
        :complexity: Best and worst case complexity is O(n * P), where n is the number 
        of teams to be generated and P is the complexity of Poketeam.random_team method.
        """
        if type(n) != int:
            raise TypeError("An integer is expected for number of teams to generate.")
        
        elif n <= 0:
            raise ValueError("An integer greater than zero (0) is expected for number of teams to generate.")

        self.teams = CircularQueue(n)
        self.teams_lives = CircularQueue(n)
        for i in range(n):
            team_name = "Team " + str(i)
            battle_mode = RandomGen.randint(0, 1)
            random_team = PokeTeam.random_team(team_name, battle_mode)
            lives = RandomGen.randint(2, 10)
            self.teams.append(random_team)
            self.teams_lives.append(lives)

    def __iter__(self) -> BattleTowerIterator:
        """ Magic method that returns a seperate iterator class to iterate 
        through the battle tower.
        :complexity: Best and worst case complexity is O(1)
        """
        return BattleTowerIterator(self.battle, self.fighting_team, self.teams, self.teams_lives)
    

""" Class for creating an iterator for the Battle Tower.
"""
class BattleTowerIterator:

    def __init__(self, battle: Battle, fighting_team: PokeTeam, teams: CircularQueue, teams_lives: CircularQueue) -> None:
        """ Method that initialises the BattleTowerIterator
        :param battle: a battle object
        :param fighting_team: the team that will fight through the tower
        :param teams: the teams in the tower 
        :param teams_lives: the lives of the respective teams in the tower
        :complexity: Best and worst case complexity is O(1)
        """
        self.battle = battle
        self.fighting_team = fighting_team
        self.teams = teams
        self.teams_lives = teams_lives
        self.prev_res = 0

    def __iter__(self) -> BattleTowerIterator:
        """ Magic iter method that returns the class itself
        :complexity: Best and worst case complexity is O(1)
        """
        return self

    def __next__(self) -> Tuple(int, str, str, int):
        """ Magic next method that returns the next item in the iterator

        :raises StopIteration: when there or no teams in the tower left or 
        the fighting team lost the previous match
        :complexity: Best and worst case complexity is O(B) where B is the complexity of battle between 
        the team and tower.
        """
        # Stop iteration if tower is empty or team lost battle in the tower
        if len(self.teams) == 0 or self.prev_res == 2:
            raise StopIteration
        
        tower_team = self.teams.serve()
        lives = self.teams_lives.serve()

        # Regenerate both teams
        self.fighting_team.regenerate_team()
        tower_team.regenerate_team()

        # Get the result of the battle
        res = self.battle.battle(self.fighting_team, tower_team)

        self.prev_res = res

        # only decrease lives if the tower team lost or drew
        if res != 2:
            lives -= 1

        me = self.fighting_team
        other = tower_team
        
        # add tower team back into the tower if they have lives left
        if lives != 0:
            self.teams.append(tower_team)
            self.teams_lives.append(lives)
    
        result = (res, me, other, lives)

        return result


    def avoid_duplicates(self) -> None:
        """ avoids duplicate teams (teams with more than one of the same pokemon type) in the
        battle tower by refactoring the tower teams.
        
        :complexity: Best and worst case complexity is O(N). Where N is the number of remaining teams in the tower.
        Reasoning for Complexity: There are two for loops so the worst case complexity is essentially O(N * n), where
        N is the reamining tower teams and n is the length of team numbers. Since that is constant and is 5 the worst case 
        complexity evaluates to O(N * 5) which becomes O(N). The best case is also O(N) if the first iteration of the second
        loop is always broken at the start of the team numbers.
        """
        tower_length = len(self.teams)
        for i in range(tower_length):
            team = self.teams.serve()
            lives = self.teams_lives.serve()
            team_numbers = team.get_team_numbers()
            duplicate = False

            # if a team number is greater than 1 then they have duplicates
            for number in team_numbers:
                if number > 1:
                    duplicate = True
                    break
            
            # add team back to the tower if they are not duplicate
            if not duplicate:
                self.teams.append(team)
                self.teams_lives.append(lives)
            

    def sort_by_lives(self):
        # 1054
        raise NotImplementedError()
