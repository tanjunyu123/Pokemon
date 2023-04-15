from __future__ import annotations
from bset import BSet

from stack_adt import ArrayStack

"""
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from poke_team import PokeTeam
from battle import Battle
from linked_list import LinkedList
from battle import Battle

class Tournament:
    
    def __init__(self, battle: Battle|None=None) -> None:
        '''Constructor for the Tournament class'''
        self.teams = None
        self.battle_mode = None
        self.tournament_list = LinkedList()

        if battle is None:
            self.battle = Battle()
        else :
            self.battle = battle

    def set_battle_mode(self, battle_mode: int) -> None:
        '''Set the battle mode that will be used for all random teams generated 
        later on for the tournamnent
        :complexity: O(1)
        '''
        self.battle_mode = battle_mode



    def is_valid_tournament(self, tournament_str: str) -> bool:
        '''Checks if the tournament string input represents a valid tournament . Return 
        True if valid, False otherwise.
        :complexity: O(N*Index) where N is the size of the input (tournament_str) '''
        str_split_postfix = tournament_str.split()

        # The teams present before converting to infix
        postfix_operands = LinkedList() 

        s = LinkedList()

        # Convert the post-fix tournament_str to infix 
        for i in str_split_postfix:
            # Push operands
            if i != '+':
                s.insert(0, i)
                postfix_operands.insert(len(postfix_operands),i)
            else:
                op1 = s[0]
                s.delete_at_index(0)
                op2 = s[0]
                s.delete_at_index(0)
                s.insert(0, "( " + op2 + " " + i + " " +
                        op1 + " )")

        result_infix = s[0][1:-1]

        str_split_infix = result_infix.split()

        # The teams present after converting the tournament_str to infix 
        infix_operands = LinkedList()

        # Insert the teams present after converting the tournament_str to infix
        for i in str_split_infix:
            if i != '+' and i != '(' and i != ')':
                infix_operands.insert(len(infix_operands),i)

        # Check if the number of teams present in the postfix_operands is the same with infix_operands 
        if len(infix_operands) == len(postfix_operands):
            return True
        else:
            return False
         

    def is_balanced_tournament(self, tournament_str: str) -> bool:
        # 1054 only
        raise NotImplementedError()

    def start_tournament(self, tournament_str: str) -> None:
        '''Start a valid tournament by generating random PokeTeams with the names following
        the tournament str (postfix) given 
        :raises TypeError : if the input is not of a string type
        :complexity : O(N*(Index) + M*Index + N*M*(Index))
        where N is the size of input tournament str
        where M is the size of the team_names or self.teams'''      
        if not type(tournament_str) == str :
            raise TypeError("A string is expected for tournament_str")

        # Check if the tournament_str is valid 
        if self.is_valid_tournament(tournament_str) :
            tournament_str_split = tournament_str.split()

            self.teams = LinkedList()
            team_names = LinkedList()

            # Retrieve the names of the poketeams given in the tournament_str and insert them into team_names
            for i in tournament_str_split :
                if i != '+' :             
                     team_names.insert(len(team_names),i)  

            # Generate random teams using the names retrieved in the team_names 
            for j in range(len(team_names)):
                poke_team = PokeTeam.random_team(team_names[j],self.battle_mode)
                self.teams.insert(len(self.teams),poke_team)

            # Insert the poketeam instances into the tournament_list in the same format as the tournament_str
            for i in range(len(tournament_str_split)):
                for j in range(len(self.teams)):
                    if tournament_str_split[i] == self.teams[j].team_name :
                        self.tournament_list.insert(i,self.teams[j])
                        break
                else:
                    self.tournament_list.insert(i,tournament_str_split[i])

    
    def advance_tournament(self) -> tuple[PokeTeam, PokeTeam, int] | None:
        '''Simulates one battle of the tournament, following the order of the previously given
        tournament string
        :complexity: O(B + P + Index)'''
 
        # Locate the position of the "+"
        try: 
            index = self.tournament_list.index("+")
        except ValueError: 
            return None # return None if no more "+" in the tournament_list. Tournament ended
        else:
            # Retrieve the 2 poketeams to battle at current turn 
            poketeam1 = self.tournament_list[index-2]
            poketeam2 = self.tournament_list[index-1]
            result = self.battle.battle(poketeam1,poketeam2)

            # Remove the poketeam that lost from the tournament_list
            if result == 1 :
                self.tournament_list.delete_at_index(index)
                self.tournament_list.remove(poketeam2)
            elif result == 2:
                self.tournament_list.delete_at_index(index)
                self.tournament_list.remove(poketeam1)

            return (poketeam1,poketeam2,result)



    def linked_list_of_games(self) -> LinkedList[tuple[PokeTeam, PokeTeam]]:
        l = LinkedList()
        while True:
            res = self.advance_tournament()
            if res is None:
                break
            l.insert(0, (res[0], res[1]))
        return l
    
    def linked_list_with_metas(self) -> LinkedList[tuple[PokeTeam, PokeTeam, list[str]]]:
        '''Seach for poketypes of pokemons that are not present in both the teams in the current battle but exist in the 
        poketeams that have lost before them in the tournament.
        :complexity: O(M*(N+(J*K*Index)+(K*N)))   where M is the total number of matches played 
                              where N is the size of the team_numbers
                              where J is the size of the battleHistory linkedList
                              where K is size of the temp linkedList '''
        l = LinkedList()

        # Store all the teams that lost in the tournament
        battleHistory = LinkedList()

        while True:
            res = self.advance_tournament()
            if res is None:
                break

            # The two teams battling at current turn 
            team1 = res[0]
            team2 = res[1]


            # Poketype not present in both the teams battling
            poketype_not_present_both_teams = BSet()

            # Poketype present in the teams that lost 
            poketype_present_team_lost = BSet()
    
            
            list_str = []

            for i in range(len(team1.team_numbers)):
                if team1.team_numbers[i] == 0 and team2.team_numbers[i] == 0:
                    if i == 0 :
                        poketype_not_present_both_teams.add(1)  # 1 represents FIRE
                    elif i == 1 :
                        poketype_not_present_both_teams.add(2)  # 2 represents GRASS
                    elif i == 2 :
                        poketype_not_present_both_teams.add(3)  # 3 represents WATER
                    elif i == 3 :
                        poketype_not_present_both_teams.add(4)  # 4 represents GHOST
                    elif i == 4 :
                        poketype_not_present_both_teams.add(5)  # 5 represents NORMAL

            temp = LinkedList()
            temp.insert(0,team1)
            temp.insert(1,team2)

            # Find the teams that lost to these 2 teams currently battling
            for i in range(len(battleHistory)-1,-1,-1):
                for j in range(len(temp)) :
                    if battleHistory[i][0].team_name == temp[j].team_name :
                        temp.insert(len(temp),battleHistory[i][1])
                    elif battleHistory[i][1].team_name == temp[j].team_name :
                        temp.insert(len(temp),battleHistory[i][0])
            
            temp.delete_at_index(0)
            temp.delete_at_index(0)

            # Find the poketypes present in the teams that lost 
            for i in range(len(temp)):
                for j in range(len(temp[i].team_numbers)) :
                    if temp[i].team_numbers[j] != 0 :
                        if j == 0 :
                            poketype_present_team_lost.add(1)
                        elif j == 1 :
                            poketype_present_team_lost.add(2)
                        elif j == 2 :
                            poketype_present_team_lost.add(3)
                        elif j == 3 :
                            poketype_present_team_lost.add(4)
                        elif j == 4 :
                            poketype_present_team_lost.add(5)

            # Poketype not present in both the teams battling but present in the teams that lost 
            result = poketype_not_present_both_teams.intersection(poketype_present_team_lost)

            if (1 in result):
                list_str.append("FIRE")
            elif (2 in result) :
                list_str.append("GRASS")
            elif (3 in result) :
                list_str.append("WATER")
            elif (4 in result) :
                list_str.append("GHOST")
            elif (5 in result) :
                list_str.append("NORMAL")

            battleHistory.insert(len(battleHistory),(team1,team2))


            l.insert(0, (res[0], res[1],list_str ))
        return l
    
    def flip_tournament(self, tournament_list: LinkedList[tuple[PokeTeam, PokeTeam]], team1: PokeTeam, team2: PokeTeam) -> None:
        # 1054
        raise NotImplementedError()

