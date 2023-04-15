"""
This module handles all battling actions between two poketeams.

Pokemons are retrieved from the poketeams and the battling continues
until at least one of the teams become empty.
"""

__author__ = "Scaffold by Jackson Goerner, Code by Rachit Bhatia"

from pokemon_base import PokemonBase
from random_gen import RandomGen
from poke_team import Action, PokeTeam, Criterion
from print_screen import print_game_screen
from linked_list import LinkedList

class Battle:
    
    def __init__(self, verbosity=0) -> None:
        pass

    def check_action_precedence(self, action1: Action, action2: Action) -> int:
        """ Compares the actions of both teams and checks the precedence order of their actions.
        
        :param team1: the first poketeam's action
        :param team2: the second poketeam' action
        :complexity: Best case = Worst case = O(I) where I is the complexity of getting the index of an item in an LinkedList
        :return: an integer which represents the order in which the team actions are executed (integer 0,1,2)
        """

        #arranging the 4 actions in a linked list in the required order of precedence
        action_list = LinkedList()
        action_list.insert(0, Action.SWAP)      #SWAP set at head - order of linked list: SWAP
        action_list.insert(0, Action.SPECIAL)   #SPECIAL set at head - order of linked list: SPECIAL, SWAP
        action_list.insert(0, Action.HEAL)      #HEAL set at head - order of linked list: HEAL, SPECIAL, SWAP
        action_list.insert(0, Action.ATTACK)    #ATTACK set at head - order of linked list: ATTACK, HEAL, SPECIAL, SWAP

        #checking the precedence based on the index of the actions stored in the linked list
        if action_list.index(action1) == action_list.index(action2):
            return 0
        elif action_list.index(action1) > action_list.index(action2):
            return 1
        elif action_list.index(action1) < action_list.index(action2):
            return 2


    def battle(self, team1: PokeTeam, team2: PokeTeam) -> int:
        """ Handles all the battle actions. 
        Calls all the necessary functions based on the selected actions and precedence, and handles the subsequent behaviours.

        :param team1: the first poketeam battling
        :param team2: the second poketeam battling
        :complexity: Best O(1) if one of the teams is empty at the start itself so the loop never runs and the other functions called also have O(1) complexity
                     Worst O(N) where N is the number of actions each team executes. N depends on the AI modes and battle modes selected for input.
        :return: the winner result (integer 0,1,2)
        """

        #initialising boolean values to see if a team used their max number of heals
        team1_used_max_heal = False
        team2_used_max_heal = False

        #initalising with False values
        both_alive = False  #both pokemons alive 
        one_alive = False   #one pokemon alive

        #retrieving pokemons from both teams
        if (not team1.is_empty()) and (not team2.is_empty()):
            pokemon1 = team1.retrieve_pokemon()
            pokemon2 = team2.retrieve_pokemon()
        
            # both booleans set to True because if retrieved, pokemons will be alive
            both_alive = True #both pokemons alive 
            one_alive = True   #one pokemon alive
        

        #while loop to manage the whole battle behaviour
        while ((not team1.is_empty()) and (not team2.is_empty())) or both_alive or one_alive:

            #resetting the variables to ensure loop behaviour is only managed by each turn's actions
            both_alive = False  
            one_alive = False   

            #retrieving new pokemon if current pokemon has fainted
            if (pokemon1.is_fainted()):
                pokemon1 = team1.retrieve_pokemon()

            if (pokemon2.is_fainted()):
                pokemon2 = team2.retrieve_pokemon()

            #getting the actions for both the teams 
            first_team_choice = team1.choose_battle_option(pokemon1, pokemon2)
            second_team_choice = team2.choose_battle_option(pokemon2, pokemon1)

            action_precedence_result = self.check_action_precedence(first_team_choice, second_team_choice)

            #if action precedence == 0, both teams execute the same actions
            if action_precedence_result == 0:
                
                if first_team_choice == Action.SWAP:

                    #swap action for a team: return a pokemon, then retreive a pokemon
                    team1.return_pokemon(pokemon1)
                    pokemon1 = team1.retrieve_pokemon()
                    team2.return_pokemon(pokemon2)
                    pokemon2 = team2.retrieve_pokemon()

                elif first_team_choice == Action.SPECIAL:

                    #special action for a team: return a pokemon, call team's special method, then retrieve a new pokemon
                    team1.return_pokemon(pokemon1)
                    team1.special()
                    pokemon1 = team1.retrieve_pokemon()
                    team2.return_pokemon(pokemon2)
                    team2.special()
                    pokemon2 = team2.retrieve_pokemon()

                elif first_team_choice == Action.HEAL:

                    #checking if any team has used their max number of heals (3)
                    if team1.num_of_heals == 0 and team2.num_of_heals == 0:
                        team1_used_max_heal = True
                        team2_used_max_heal = True 
                        break   #break out of the loop once a team has used 3 heals because that team loses
                    elif team1.num_of_heals == 0:
                        team1_used_max_heal = True
                        break
                    elif team2.num_of_heals == 0:
                        team2_used_max_heal = True
                        break

                    #heal action for a team: heal and then reduce the number of heals by 1
                    pokemon1.heal()
                    team1.num_of_heals -= 1    #reduce by 1 to account for total heals used by the team
                    pokemon2.heal()
                    team2.num_of_heals -= 1
                    
                elif first_team_choice == Action.ATTACK:
                    self.both_attack(pokemon1, pokemon2)  #both teams attack
               

            #team 1 action is executed first due to higher action precedence
            #hence, checking for team 1 actions before team 2
            elif action_precedence_result == 1:
                if first_team_choice == Action.SWAP:
                    #swap action for a team: return a pokemon, then retreive a pokemon
                    team1.return_pokemon(pokemon1)
                    pokemon1 = team1.retrieve_pokemon()

                elif first_team_choice == Action.SPECIAL:
                    #special action for a team: return a pokemon, call team's special method, then retrieve a new pokemon
                    team1.return_pokemon(pokemon1)
                    team1.special()
                    pokemon1 = team1.retrieve_pokemon()

                elif first_team_choice == Action.HEAL:
                    #checking if the team has used their max number of heals (3)
                    if team1.num_of_heals == 0:
                        team1_used_max_heal = True
                        break  #break out of the loop once 3 heals used because team 1 loses

                    pokemon1.heal()
                    team1.num_of_heals -= 1  #reduce by 1 to account for total heals used by the team

                #attack action for a single team attacking the other
                elif first_team_choice == Action.ATTACK:
                    pokemon1.attack(pokemon2)  #calling the attack function to make team 1's pokemon attack team 2's pokemon

                #team 2 actions are checked and executed after team 1
                if second_team_choice == Action.SWAP:
                    team2.return_pokemon(pokemon2)
                    pokemon2 = team2.retrieve_pokemon()

                elif second_team_choice == Action.SPECIAL:
                    team2.return_pokemon(pokemon2)
                    team2.special()
                    pokemon2 = team2.retrieve_pokemon()

                elif second_team_choice == Action.HEAL:
                    if team2.num_of_heals == 0:
                        team2_used_max_heal = True
                        break

                    pokemon2.heal()
                    team2.num_of_heals -= 1

                elif second_team_choice == Action.ATTACK:
                    pokemon2.attack(pokemon1)   #calling the attack function to make team 2's pokemon attack team 1's pokemon


            #team 2 action is executed first due to higher action precedence
            #hence, checking for team 2 actions before team 1
            elif action_precedence_result == 2:
                if second_team_choice == Action.SWAP:
                    team2.return_pokemon(pokemon2)
                    pokemon2 = team2.retrieve_pokemon()

                elif second_team_choice == Action.SPECIAL:
                    team2.return_pokemon(pokemon2)
                    team2.special()
                    pokemon2 = team2.retrieve_pokemon()

                elif second_team_choice == Action.HEAL:
                    if team2.num_of_heals == 0:
                        team2_used_max_heal = True
                        break

                    pokemon2.heal()
                    team2.num_of_heals -= 1

                #attack action for a single team attacking the other
                elif second_team_choice == Action.ATTACK:
                    pokemon2.attack(pokemon1)   #calling the attack function to make team 2's pokemon attack team 1's pokemon

                #team 1 actions are checked and executed after team 2
                if first_team_choice == Action.SWAP:
                    team1.return_pokemon(pokemon1)
                    pokemon1 = team1.retrieve_pokemon()


                elif first_team_choice == Action.SPECIAL:
                    team1.return_pokemon(pokemon1)
                    team1.special()
                    pokemon1 = team1.retrieve_pokemon()

                elif first_team_choice == Action.HEAL:
                    if team1.num_of_heals == 0:
                        team1_used_max_heal = True
                        break

                    pokemon1.heal()
                    team1.num_of_heals -= 1

                elif first_team_choice == Action.ATTACK:
                    c = pokemon2.get_hp()
                    pokemon1.attack(pokemon2)
                    d = pokemon2.get_hp()
            
            #checking level up and evolved versions after battling between the pokemons has finished for the current round
            if (not pokemon1.is_fainted()) and (not pokemon2.is_fainted()):
                #both pokemons lose 1 hp if they are both alive
                pokemon1.lose_hp(1)
                pokemon2.lose_hp(1)
                if (not pokemon1.is_fainted()) and (not pokemon2.is_fainted()):
                    both_alive = True #setting both_alive to true when both pokemons are alive so that while loop continues

            #behaviours for the case where team 1 pokemon faints after the current round
            if pokemon1.is_fainted() and not pokemon2.is_fainted():
                pokemon2.level_up()     #team 2 pokemon levels up if team 1 pokemon is fainted
                
                team1.return_pokemon(pokemon1)  #return team 1's fainted pokemon

                if team1.is_empty():
                    team2.return_pokemon(pokemon2) #return team 2's pokemon if team 1 is empty because team 2 won so winner pokemon must be returned
                
                if team2.is_empty():
                    one_alive = True  #set one pokemon alive to true so that loop continues even if team 2 only has one remaining alive pokemon and is on the battlefield

            #behaviours for the case where team 2 pokemon faints after the current round
            elif pokemon2.is_fainted() and not pokemon1.is_fainted():
                pokemon1.level_up()     #team 1 pokemon levels up if team 2 pokemon is fainted

                team2.return_pokemon(pokemon2)   #return team 2's fainted pokemon

                if team2.is_empty():
                    team1.return_pokemon(pokemon1) #return team 1's pokemon if team 2 is empty because team 1 won so winner pokemon must be returned
                
                if team1.is_empty():
                    one_alive = True #set one pokemon alive to true so that loop continues even if team 1 only has one remaining alive pokemon and is on the battlefield

            #behaviours for the case where both pokemons faint after the current round
            elif pokemon1.is_fainted() and pokemon2.is_fainted():
                #return both fainted pokemons (they don't get returned to the team)
                team1.return_pokemon(pokemon1)
                team2.return_pokemon(pokemon2)
            
            #checking if team 1's pokemon can evolve after the current battle round
            if not pokemon1.is_fainted():
                if pokemon1.can_evolve() and pokemon1.should_evolve():  #evolve if pokemon is evolvable and meets requirements to evolve
                    pokemon1 = pokemon1.get_evolved_version() 

            #checking if team 2's pokemon can evolve after the current battle round
            if not pokemon2.is_fainted():
                if pokemon2.can_evolve() and pokemon2.should_evolve():  #evolve if pokemon is evolvable and meets requirements to evolve
                    pokemon2 = pokemon2.get_evolved_version()
            
    ####-End of While Loop-####
                
        ####--Deciding winner of battle--####

        if (team1_used_max_heal and team2_used_max_heal):
            winner_result = 0   #if both teams have used 3 heals, result is draw
        elif (team2_used_max_heal):
            winner_result = 1   #if team 2 has used 3 heals, team 1 wins
        elif (team1_used_max_heal):
            winner_result = 2   #if team 1 has used 3 heals, team 2 wins
            
        elif (team1.is_empty() and team2.is_empty()):
            winner_result = 0  #if both teams are empty, result is draw
        elif team2.is_empty() and not team1.is_empty():
            winner_result = 1  #if team 2 is empty, team 1 wins
        elif team1.is_empty() and not team2.is_empty():
            winner_result = 2  #if team 1 is empty, team 2 wins

        return winner_result
        
    def both_attack(self, first_pokemon: PokemonBase, second_pokemon: PokemonBase):
        """  Defines the behaviour when both teams attack each other (both teams choose ATTACK action).

        :param first_pokemon: the pokemon from team 1
        :param second_pokemon: the pokemon from team 2
        :complexity: Best Case = Worst Case = O(1) because all other functions called are also O(1), there
                     are no loops invoved, and there are no conditions which make the function exit early.
        """
        
        #obtaining the speeds of both teams pokemons to check which team attacks first
        pokemon1_speed = first_pokemon.get_speed()
        pokemon2_speed = second_pokemon.get_speed()

        #if team 1 pokemon has higher speed, it attacks first
        if pokemon1_speed > pokemon2_speed:
            first_pokemon.attack(second_pokemon) #team 1 pokemon attacks team 2 pokemon
            if not second_pokemon.is_fainted():  
                second_pokemon.attack(first_pokemon) #if team 2 pokemon is alive after getting attacked, it attacks back
        
        #if team 2 pokemon has higher speed, it attacks first
        elif pokemon2_speed > pokemon1_speed:
            second_pokemon.attack(first_pokemon) #team 2 pokemon attacks team 1 pokemon
            if not first_pokemon.is_fainted():
                first_pokemon.attack(second_pokemon) #if team 1 pokemon is alive after getting attacked, it attacks back

        #both teams attack if their pokemons have the same speeds
        elif pokemon1_speed == pokemon2_speed:
            first_pokemon.attack(second_pokemon) #team 1's attack is processed first
            second_pokemon.attack(first_pokemon) #team 2 pokemon attacks even if it faints



if __name__ == "__main__":
    b = Battle(verbosity=3)
    RandomGen.set_seed(16)
    t1 = PokeTeam.random_team("Cynthia", 0, criterion=Criterion.SPD)
    t1.ai_type = PokeTeam.AI.USER_INPUT
    t2 = PokeTeam.random_team("Barry", 1)
    print(b.battle(t1, t2))


