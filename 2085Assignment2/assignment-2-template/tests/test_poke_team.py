from poke_team import Action, Criterion, PokeTeam
from random_gen import RandomGen
from pokemon import Bulbasaur, Charizard, Charmander, Gastly, Squirtle, Eevee
from tests.base_test import BaseTest

class TestPokeTeam(BaseTest):

    def test_random(self):
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Cynthia", 0)
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Squirtle, Gastly, Eevee, Eevee, Eevee, Eevee]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_regen_team(self):
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Cynthia", 2, team_size=4, criterion=Criterion.HP)
        # This should end, since all pokemon are fainted, slowly.
        while not t.is_empty():
            p = t.retrieve_pokemon()
            p.lose_hp(1)
            t.return_pokemon(p)
        t.regenerate_team()
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Bulbasaur, Eevee, Charmander, Gastly]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_battle_option_attack(self):
        t = PokeTeam("Wallace", [1, 0, 0, 0, 0], 1, PokeTeam.AI.ALWAYS_ATTACK)
        p = t.retrieve_pokemon()
        e = Eevee()
        self.assertEqual(t.choose_battle_option(p, e), Action.ATTACK)

    def test_special_mode_1(self):
        t = PokeTeam("Lance", [1, 1, 1, 1, 1], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        # C B S G E
        t.special()
        # S G E B C
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Squirtle, Gastly, Eevee, Bulbasaur, Charmander]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_string(self):
        t = PokeTeam("Dawn", [1, 1, 1, 1, 1], 2, PokeTeam.AI.RANDOM, Criterion.DEF)
        self.assertEqual(str(t), "Dawn (2): [LV. 1 Gastly: 6 HP, LV. 1 Squirtle: 11 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP]")
        
    ###########################################################
    ################ Personal Designed Tests ##################
    
    def test_special_mode_2_raise_error(self):
        """ Test that an exception is raised when a criterion is not specified for battle mode 2"""

        self.assertRaises(Exception, lambda:PokeTeam("Shyam", [1, 1, 1, 1, 1], 2, PokeTeam.AI.ALWAYS_ATTACK))

    def test_special_mode_2(self):
        """ Test the battle mode 2 ordering of pokemon accoring to their speed."""

        t = PokeTeam("Shyam", [1, 1, 1, 1, 1], 2, PokeTeam.AI.ALWAYS_ATTACK, criterion = Criterion.SPD)
        self.assertEqual(str(t), "Shyam (2): [LV. 1 Charmander: 9 HP, LV. 1 Eevee: 10 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP]")
        # C E B S G
        t.special()
        # G S B E C
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Gastly, Squirtle, Bulbasaur, Eevee, Charmander]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)
    
    def test_retrieving_and_returning(self):
        """ Test that the retrieving and returning of pokmeon for each type of battle mode is valid 
        and accurate.
        """
        t1 = PokeTeam("Jun Yu", [1, 2, 0, 1, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        t2 = PokeTeam("Rachit", [1, 1, 1, 1, 1], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        t3 = PokeTeam("Shyam", [0, 1, 1, 1, 1], 2, PokeTeam.AI.ALWAYS_ATTACK, criterion = Criterion.SPD)

        # Team 1 retrieve and return with battle mode 0
        p = t1.retrieve_pokemon()
        self.assertIsInstance(p, Charmander)
        t1.return_pokemon(p)
        p = t1.retrieve_pokemon()
        self.assertIsInstance(p, Charmander)

        # Team 2 retrieve and return with battle mode 1
        p = t2.retrieve_pokemon()
        self.assertIsInstance(p, Charmander)
        t2.return_pokemon(p)
        p = t2.retrieve_pokemon()
        self.assertIsInstance(p, Bulbasaur)

        # Team 3 retrieve and return with battle mode 2
        p = t3.retrieve_pokemon()
        self.assertIsInstance(p, Eevee)
        t3.return_pokemon(p)
        p = t3.retrieve_pokemon()
        self.assertIsInstance(p, Eevee)
    
    def test_special_mode_0(self):
        """ Test special of battle mode 0"""
        t = PokeTeam("Jun Yu", [1, 0, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        # C S G E
        t.special()
        # E S G C
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Eevee, Squirtle, Gastly, Charmander]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)
    
    def test_random_team(self):
        """ Test a random poke team"""

        RandomGen.set_seed(51234)
        t = PokeTeam.random_team("N", 2, team_size=6, criterion=Criterion.HP)
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Bulbasaur, Bulbasaur, Bulbasaur, Squirtle, Gastly, Gastly]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)
