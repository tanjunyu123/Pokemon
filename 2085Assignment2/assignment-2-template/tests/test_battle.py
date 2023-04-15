from random_gen import RandomGen
from battle import Battle
from poke_team import Criterion, PokeTeam
from pokemon import Bulbasaur, Charizard, Charmander, Eevee, Gastly, Haunter, Squirtle, Venusaur
from tests.base_test import BaseTest

class TestBattle(BaseTest):

    def test_basic_battle(self):
        RandomGen.set_seed(1337)
        team1 = PokeTeam("Ash", [1, 1, 1, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        team2 = PokeTeam("Gary", [0, 0, 0, 0, 3], 0, PokeTeam.AI.ALWAYS_ATTACK)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 1)
        self.assertTrue(team2.is_empty())
        remaining = []
        while not team1.is_empty():
            remaining.append(team1.retrieve_pokemon())
        self.assertEqual(len(remaining), 2)
        self.assertEqual(remaining[0].get_hp(), 1)
        self.assertIsInstance(remaining[0], Venusaur)
        self.assertEqual(remaining[1].get_hp(), 11)
        self.assertIsInstance(remaining[1], Squirtle)

    def test_complicated_battle(self):
        RandomGen.set_seed(192837465)
        team1 = PokeTeam("Brock", [1, 1, 1, 1, 1], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, criterion=Criterion.HP)
        team2 = PokeTeam("Misty", [0, 0, 0, 3, 3], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, criterion=Criterion.SPD)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 1)
        remaining = []
        while not team1.is_empty():
            remaining.append(team1.retrieve_pokemon())
        self.assertEqual(len(remaining), 2)
        self.assertEqual(remaining[0].get_hp(), 11)
        self.assertIsInstance(remaining[0], Charizard)
        self.assertEqual(remaining[1].get_hp(), 6)
        self.assertIsInstance(remaining[1], Gastly)

    ###########################################################
    ################ Personal Designed Tests ##################

    def test_basic_battle2(self):
        """
        Test to check the behaviour when team 2 wins
        """
        RandomGen.set_seed(20)
        team1 = PokeTeam("Ash", [0, 1, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        team2 = PokeTeam("Gary", [1, 1, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 2)  #team 2 wins
        self.assertTrue(team1.is_empty())
        remaining = []
        while not team2.is_empty():
            remaining.append(team2.retrieve_pokemon())
        self.assertEqual(len(remaining), 2)
        self.assertEqual(remaining[0].get_hp(), 10)
        self.assertIsInstance(remaining[0], Charmander)


    def test_basic_battle3(self):
        """
        Test to check the behaviour when there is a draw
        """
        RandomGen.set_seed(2828)
        team1 = PokeTeam("Kevin", [1, 0, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        team2 = PokeTeam("Holt", [1, 0, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 0)  #draw
        self.assertTrue(team1.is_empty())
        self.assertTrue(team2.is_empty())


    def test_both_teams_empty(self):
        """
        Test to check the behaviour when both teams are empty from the start
        """
        RandomGen.set_seed(2828)
        team1 = PokeTeam("John", [0, 0, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        team2 = PokeTeam("Shyam", [0, 0, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 0)  #draw
        self.assertTrue(team1.is_empty())
        self.assertTrue(team2.is_empty())


    def test_battle_mode_1_and_super_effective(self):
        """
        Test to check the battle behaviour when battle mode 1 is selected and the AI modes are set as swap on super effective
        """
        RandomGen.set_seed(3129)
        team1 = PokeTeam("Rachit", [0, 2, 0, 0, 0], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        team2 = PokeTeam("Jun Yu", [0, 0, 0, 3, 0], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 2)  #team 2 wins
        self.assertTrue(team1.is_empty())
        remaining = []
        while not team2.is_empty():
            remaining.append(team2.retrieve_pokemon())
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].get_hp(), 8)
        self.assertIsInstance(remaining[0], Haunter)


    def test_complicated_battle2(self):
        """
        Test to check for a complicated battle where both teams have varying pokemon distibution, different battle modes and different AI modes
        """
        RandomGen.set_seed(9976)
        team1 = PokeTeam("Jobin", [1, 2, 0, 1, 0], 1, PokeTeam.AI.RANDOM)
        team2 = PokeTeam("Rachit", [3, 0, 0, 3, 0], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, criterion=Criterion.LV)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 2)  #team 2 wins
        self.assertTrue(team1.is_empty())
        remaining = []
        while not team2.is_empty():
            remaining.append(team2.retrieve_pokemon())
        self.assertEqual(len(remaining), 6)
        self.assertEqual(remaining[0].get_hp(), 17)
        self.assertIsInstance(remaining[0], Charizard)

        self.assertEqual(remaining[1].get_hp(), 9)
        self.assertIsInstance(remaining[1], Charmander)

        self.assertEqual(remaining[2].get_hp(), 6)
        self.assertIsInstance(remaining[2], Gastly)

        self.assertEqual(remaining[3].get_hp(), 6)
        self.assertIsInstance(remaining[3], Gastly)

        self.assertEqual(remaining[4].get_hp(), 6)
        self.assertIsInstance(remaining[4], Gastly)

        self.assertEqual(remaining[5].get_hp(), 9)
        self.assertIsInstance(remaining[5], Charmander)

    
    def test_complicated_battle3(self):
        """
        This test covers both teams having all 5 types of pokemons and using Random AI mode so that HEAL mode can also be tested
        """ 
        RandomGen.set_seed(61509)
        team1 = PokeTeam("Jun Yu", [1, 2, 1, 1, 1], 2, PokeTeam.AI.RANDOM, criterion=Criterion.DEF)
        team2 = PokeTeam("Shyam", [1, 1, 1, 2, 1], 2, PokeTeam.AI.RANDOM, criterion=Criterion.LV)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 1)  #team 1 wins
        self.assertTrue(team2.is_empty())
        remaining = []
        while not team1.is_empty():
            remaining.append(team1.retrieve_pokemon())
        self.assertEqual(len(remaining), 4)
        self.assertEqual(remaining[0].get_hp(), 7)
        self.assertIsInstance(remaining[0], Haunter)

        self.assertEqual(remaining[1].get_hp(), 11)
        self.assertIsInstance(remaining[1], Squirtle)

        self.assertEqual(remaining[2].get_hp(), 15)
        self.assertIsInstance(remaining[2], Venusaur)

        self.assertEqual(remaining[3].get_hp(), 13)
        self.assertIsInstance(remaining[3], Venusaur)


    def test_random_teams_battle(self):
        """
        Test to check if battle behaviour works correctly between randomly generated teams
        """
        RandomGen.set_seed(12431)
        team1 = PokeTeam.random_team("Rachit", 1, 4, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        team2 = PokeTeam.random_team("Jun Yu", 1, 3, PokeTeam.AI.RANDOM)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 1)  #team 1 wins
        self.assertTrue(team2.is_empty())
        remaining = []
        while not team1.is_empty():
            remaining.append(team1.retrieve_pokemon())
        self.assertEqual(len(remaining), 3)
        self.assertEqual(remaining[0].get_hp(), 10)
        self.assertIsInstance(remaining[0], Eevee)

        self.assertEqual(remaining[1].get_hp(), 11)
        self.assertIsInstance(remaining[1], Squirtle)

        self.assertEqual(remaining[2].get_hp(), 5)
        self.assertIsInstance(remaining[2], Eevee)


    def test_random_teams_battle2(self):
        """
        Test to check if battle behaviour works correctly between randomly generated teams
        """
        RandomGen.set_seed(321486)
        team1 = PokeTeam.random_team("Rachit", 0, None, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        team2 = PokeTeam.random_team("Jun Yu", 2, None, PokeTeam.AI.RANDOM, criterion= Criterion.SPD)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 2)  #team 2 wins
        self.assertTrue(team1.is_empty())
        remaining = []
        while not team2.is_empty():
            remaining.append(team2.retrieve_pokemon())
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].get_hp(), 6)
        self.assertIsInstance(remaining[0], Venusaur)
