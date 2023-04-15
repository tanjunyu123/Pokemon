from random_gen import RandomGen
from tournament import Tournament
from battle import Battle
from tests.base_test import BaseTest

class TestTournament(BaseTest):

    def test_creation(self):
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertRaises(ValueError, lambda: t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + + + Fantina Byron + Candice Volkner + + +"))
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")

    def test_random(self):
        RandomGen.set_seed(123456)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")

        team1, team2, res = t.advance_tournament() # Roark vs Gardenia
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Roark"))
        self.assertTrue(str(team2).startswith("Gardenia"))

        team1, team2, res = t.advance_tournament() # Maylene vs Crasher_Wake
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Maylene"))
        self.assertTrue(str(team2).startswith("Crasher_Wake"))

        team1, team2, res = t.advance_tournament() # Fantina vs Byron
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Fantina"))
        self.assertTrue(str(team2).startswith("Byron"))

        team1, team2, res = t.advance_tournament() # Maylene vs Fantina
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Maylene"))
        self.assertTrue(str(team2).startswith("Fantina"))

        team1, team2, res = t.advance_tournament() # Roark vs Fantina
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Roark"))
        self.assertTrue(str(team2).startswith("Fantina"))

        team1, team2, res = t.advance_tournament() # Candice vs Volkner
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Candice"))
        self.assertTrue(str(team2).startswith("Volkner"))

        team1, team2, res = t.advance_tournament() # Roark vs Candice
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Roark"))
        self.assertTrue(str(team2).startswith("Candice"))

    def test_metas(self):
        RandomGen.set_seed(123456)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")
        l = t.linked_list_with_metas()
        # Roark = [0, 2, 1, 1, 1]
        # Garderia = [0, 0, 2, 0, 1]
        # Maylene = [6, 0, 0, 0, 0]
        # Crasher_Wake = [0, 2, 0, 1, 0]
        # Fantina = [0, 0, 1, 1, 1]
        # Byron = [0, 2, 0, 0, 1]
        # Candice = [2, 2, 1, 0, 0]
        # Volkner = [0, 5, 0, 0, 0]
        expected = [
            [],
            [],
            ['FIRE'], # Roark Fantina do not have Fire types, but Maylene does (lost to Fantina)
            ['GRASS'], # Maylene Fantina do not have Grass types, but Byron/Crasher_Wake does (lost to Fantina/Maylene)
            [],
            [],
            [],
        ]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types)

    def test_balance(self):
        # 1054
        t = Tournament()
        self.assertFalse(t.is_balanced_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +"))


    ###########################################################
    ################ Personal Designed Tests ##################
    
    # Test set_battle_mode function
    def set_battle_mode_0(self):
        tournament = Tournament(Battle(verbosity=0))
        tournament.set_battle_mode(0)
        self.assertEqual(tournament.battle_mode,0)

    def set_battle_mode_1(self):
        tournament = Tournament(Battle(verbosity=0))
        tournament.set_battle_mode(1)
        self.assertEqual(tournament.battle_mode,1)
    
    def set_battle_mode_2(self):
        tournament = Tournament(Battle(verbosity=0))
        tournament.set_battle_mode(2)
        self.assertEqual(tournament.battle_mode,2)

    # Test start_tournament function and is_valid_tournament function

    # Test description: Tournament started with an invalid tournament_str that has more '+' operator than necessary
    def test_start_tournament_invalid_tournament_str_1(self):
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertRaises(ValueError, lambda: t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina + + +"))

    # Test description: Tournament started with an invalid tournament_str that has insufficient '+' operator 
    def test_start_tournament_invalid_tournament_str_2(self):
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertFalse(t.start_tournament("Roark Gardenia + Maylene Crasher_Wake"))

    # Test description: Tournament started with a valid tournament_str
    def test_start_tournament_valid_tournament_str(self):
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertEqual(t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + +"),None)


    # Test advance_tournament 
    def test_random_1(self):
        RandomGen.set_seed(2468)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Anthony James + Yessirr What + +")

        team1, team2, res = t.advance_tournament() # Anthony vs James
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Anthony"))
        self.assertTrue(str(team2).startswith("James"))

        team1, team2, res = t.advance_tournament() # Yessirr vs What
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Yessirr"))
        self.assertTrue(str(team2).startswith("What"))

        team1, team2, res = t.advance_tournament() # James vs What
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("James"))
        self.assertTrue(str(team2).startswith("What"))

    def test_random_2(self):
        RandomGen.set_seed(3579)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("How Rachit + Shyam Jobin + + Wait Random + +")

        team1, team2, res = t.advance_tournament() # How vs Rachit
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("How"))
        self.assertTrue(str(team2).startswith("Rachit"))

        team1, team2, res = t.advance_tournament() # Shyam vs Jobin
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Shyam"))
        self.assertTrue(str(team2).startswith("Jobin"))

        team1, team2, res = t.advance_tournament() # Rachit vs Shyam
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Rachit"))
        self.assertTrue(str(team2).startswith("Shyam"))

        team1, team2, res = t.advance_tournament() # Wait vs Random
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Wait"))
        self.assertTrue(str(team2).startswith("Random"))

        team1, team2, res = t.advance_tournament() # Shyam vs Random
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Shyam"))
        self.assertTrue(str(team2).startswith("Random"))


    def test_random_3(self):
        RandomGen.set_seed(6453634)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Okay Nope + Lol Why + Can Really + + +")

        team1, team2, res = t.advance_tournament() # Okay vs Nope
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Okay"))
        self.assertTrue(str(team2).startswith("Nope"))

        team1, team2, res = t.advance_tournament() # Lol vs Why
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Lol"))
        self.assertTrue(str(team2).startswith("Why"))

        team1, team2, res = t.advance_tournament() # Can vs Really
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Can"))
        self.assertTrue(str(team2).startswith("Really"))

        team1, team2, res = t.advance_tournament() # Lol vs Can
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Lol"))
        self.assertTrue(str(team2).startswith("Can"))

        team1, team2, res = t.advance_tournament() # Okay vs Can
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Okay"))
        self.assertTrue(str(team2).startswith("Can"))


    # Test linked_list_with_metas
    def test_metas_1(self):
        RandomGen.set_seed(2468)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Anthony James + Yessirr What + +")
        
        l = t.linked_list_with_metas()

        # Anthony = [1, 1, 2, 0, 0]
        # James = [0, 1, 0, 2, 3]
        # Yessirr = [2, 0, 0, 3, 0]
        # What = [0, 1, 1, 3, 1]
        expected = [
            ['FIRE'], # James and What do not have Fire types, but Anthony and Yessir do (lost to James and What)
            [],
            [],
        ]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types)


    def test_metas_2(self):
        RandomGen.set_seed(3579)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        t.start_tournament("How Rachit + Shyam Jobin + + Wait Random + +")
    
        l = t.linked_list_with_metas()
   
        # How = [0, 1, 0, 1, 2]
        # Rachit = [1, 1, 3, 1, 0]
        # Shyam = [1, 3, 0, 1, 1]
        # Jobin = [0, 1, 1, 0, 1]
        # Wait = [1, 1, 2, 0, 0]
        # Random = [1, 0, 2, 1, 0]
        expected = [
            [],
            [],
            [],
            [],
            [],
        ]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types)

    def test_metas_3(self):
        RandomGen.set_seed(6453634)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Okay Nope + Lol Why + Can Really + + +")
        l = t.linked_list_with_metas()

        # Okay = [0, 1, 1, 1, 0]
        # Nope = [0, 0, 4, 1, 0]
        # Lol = [0, 2, 2, 1, 1]
        # Why = [0, 1, 3, 0, 0]
        # Can = [2, 1, 2, 1, 0]
        # Really [0, 2, 0, 3, 0]
        expected = [
            ['NORMAL'], # Okay and Can do not have Normal type, but Lol does (lost to Can)
            [],
            [],
            [],
            [],
        ]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types)

       