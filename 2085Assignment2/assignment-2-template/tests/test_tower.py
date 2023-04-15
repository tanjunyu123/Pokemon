from random_gen import RandomGen
from poke_team import Criterion, PokeTeam
from battle import Battle
from tower import BattleTower
from tests.base_test import BaseTest

class TestTower(BaseTest):

    def test_creation(self):
        RandomGen.set_seed(51234)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("N", 2, team_size=6, criterion=Criterion.HP))
        bt.generate_teams(4)
        # Teams have 7, 10, 10, 3 lives.
        RandomGen.set_seed(1029873918273)
        results = [
            (1, 6),
            (1, 9),
            (2, 10)
        ]
        it = iter(bt)
        for (expected_res, expected_lives), (res, me, tower, lives) in zip(results, it):
            self.assertEqual(expected_res, res, (expected_res, expected_lives))
            self.assertEqual(expected_lives, lives)

    def test_duplicates(self):
        RandomGen.set_seed(29183712400123)
    
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("Jackson", 0, team_size=6))
        bt.generate_teams(10)

        # Team numbers before:
        # [0, 4, 1, 0, 0], 6
        # [1, 0, 2, 0, 0], 5
        # [1, 1, 0, 1, 0], 8
        # [1, 2, 1, 1, 0], 10
        # [0, 0, 2, 1, 1], 8
        # [1, 1, 3, 0, 0], 4
        # [0, 2, 0, 1, 0], 5
        # [1, 0, 0, 4, 0], 3
        # [1, 1, 1, 0, 2], 7
        # [0, 1, 1, 1, 0], 9
        it = iter(bt)
        it.avoid_duplicates()
        # Team numbers after:
        # [1, 1, 0, 1, 0], 8
        # [0, 1, 1, 1, 0], 9

        l = []
        for res, me, tower, lives in bt:
            tower.regenerate_team()
            l.append((res, lives))
        
        self.assertEqual(l, [
            (1, 7),
            (1, 8),
            (2, 7)
        ])
        
    def test_sort_lives(self):
        # 1054 only
        RandomGen.set_seed(9821309123)
    
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("Jackson", 1, team_size=6))
        bt.generate_teams(10)

        it = iter(bt)
        # [1, 1, 3, 0, 0] 3 Name: Team 0
        # [2, 1, 0, 1, 0] 2 Name: Team 1
        # [2, 0, 0, 1, 1] 4 Name: Team 2
        # [3, 0, 1, 0, 1] 2 Name: Team 3
        # [0, 0, 2, 1, 2] 4 Name: Team 4
        # [0, 1, 0, 2, 0] 3 Name: Team 5
        # [3, 0, 2, 0, 0] 8 Name: Team 6
        # [0, 0, 2, 1, 0] 4 Name: Team 7
        # [0, 2, 1, 1, 0] 3 Name: Team 8
        # [1, 0, 1, 3, 1] 4 Name: Team 9
        RandomGen.set_seed(123)
        res, me, other_1, lives = next(it)
        it.sort_by_lives()
        # [1, 1, 3, 0, 0] 2 Name: Team 0
        # [2, 1, 0, 1, 0] 2 Name: Team 1
        # [3, 0, 1, 0, 1] 2 Name: Team 3
        # [0, 1, 0, 2, 0] 3 Name: Team 5
        # [0, 2, 1, 1, 0] 3 Name: Team 8
        # [2, 0, 0, 1, 1] 4 Name: Team 2
        # [0, 0, 2, 1, 2] 4 Name: Team 4
        # [0, 0, 2, 1, 0] 4 Name: Team 7
        # [1, 0, 1, 3, 1] 4 Name: Team 9
        # [3, 0, 2, 0, 0] 8 Name: Team 6
        res, me, other_2, lives = next(it)

        self.assertEqual(str(other_1), str(other_2))
    
    ###########################################################
    ################ Personal Designed Tests ##################
    
    def test_generate_type_error(self):
        """ Test that generate function of BattleTower only takes in integers"""
        bt = BattleTower(Battle(verbosity=0))
        self.assertRaises(TypeError, lambda: bt.generate_teams("5"))

    def test_generate_value_error(self):
        """ Test that generate function of BattleTower only takes in integers greater than zero"""
        bt = BattleTower(Battle(verbosity=0))
        self.assertRaises(ValueError, lambda: bt.generate_teams(-1))

    def test_creation_1(self):
        """ Test tower for battle mode 0 fighting team and a tower of 3 teams"""
        RandomGen.set_seed(634)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("Shyam", 0, team_size=5))
        bt.generate_teams(3)
        self.assertEqual(len(bt.teams), 3) # check if the correct number of teams has been generated
        RandomGen.set_seed(456567)
        results = [
            (1, 7),
            (2, 9)
        ]
        it = iter(bt)
        for (expected_res, expected_lives), (res, me, tower, lives) in zip(results, it):
            self.assertEqual(expected_res, res, (expected_res, expected_lives))
            self.assertEqual(expected_lives, lives)

    def test_creation_2(self):
        """ Test tower for battle mode 1 fighting team and a tower of 2 teams"""
        RandomGen.set_seed(23424)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("Jobin", 1, team_size=2))
        bt.generate_teams(2)
        self.assertEqual(len(bt.teams), 2) # check if the correct number of teams has been generated
        RandomGen.set_seed(86547)
        results = [
            (2, 4)
        ]
        it = iter(bt)
        for (expected_res, expected_lives), (res, me, tower, lives) in zip(results, it):
            self.assertEqual(expected_res, res, (expected_res, expected_lives))
            self.assertEqual(expected_lives, lives)

    def test_creation_3(self):
        """ Test tower for battle mode 2 fighting team and a tower of 1 team"""
        RandomGen.set_seed(1234451515)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("Jun Yu", 2, team_size=4, criterion=Criterion.DEF))
        bt.generate_teams(1)
        self.assertEqual(len(bt.teams), 1) # check if the correct number of teams has been generated
        RandomGen.set_seed(15151515265261)
        results = [
            (1, 9),
            (1, 8),
            (2, 8)
        ]
        it = iter(bt)
        for (expected_res, expected_lives), (res, me, tower, lives) in zip(results, it):
            self.assertEqual(expected_res, res, (expected_res, expected_lives))
            self.assertEqual(expected_lives, lives)
    
    def test_duplicates_1(self):
        """ Test if the duplicates are removed appropriately with 6 tower teams"""
        RandomGen.set_seed(235)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("Jun Yu", 2, team_size=4, criterion=Criterion.DEF))
        bt.generate_teams(6)
        RandomGen.set_seed(246363)

        # The team numbers of the tower before removing the duplicates
        before_duplicate = [[0, 1, 0, 1, 2], 
                            [1, 1, 1, 0, 0],
                            [0, 0, 1, 3, 0],
                            [0, 1, 1, 1, 0],
                            [1, 4, 0, 0, 0],
                            [0, 0, 1, 1, 2]]
        # The team numbers of the tower after removing the duplicates
        after_duplicate = [[1, 1, 1, 0, 0],
                           [0, 1, 1, 1, 0]]

        for i in (range(len(bt.teams))):
            team = bt.teams.serve()
            self.assertEqual(team.get_team_numbers(), before_duplicate[i])
            bt.teams.append(team)
        
        it = iter(bt)
        it.avoid_duplicates()
        
        for i in (range(len(bt.teams))):
            team = bt.teams.serve()
            self.assertEqual(team.get_team_numbers(), after_duplicate[i])
            bt.teams.append(team)

    def test_duplicates_2(self):
        """ Test if the duplicates are removed  with 3 tower teams"""
        RandomGen.set_seed(546)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("Jun Yu", 2, team_size=4, criterion=Criterion.DEF))
        bt.generate_teams(3)
        RandomGen.set_seed(3462626)

        # The team numbers of the tower before removing the duplicates
        before_duplicate = [[0, 0, 0, 3, 0],
                            [1, 1, 0, 1, 0],
                            [1, 0, 0, 3, 2]]

        # The team numbers of the tower after removing the duplicates           
        after_duplicate = [[1, 1, 0, 1, 0]]

        for i in (range(len(bt.teams))):
            team = bt.teams.serve()
            self.assertEqual(team.get_team_numbers(), before_duplicate[i])
            bt.teams.append(team)
        
        it = iter(bt)
        it.avoid_duplicates()
        
        for i in (range(len(bt.teams))):
            team = bt.teams.serve()
            self.assertEqual(team.get_team_numbers(), after_duplicate[i])
            bt.teams.append(team)

    def test_duplicates_3(self):
        """ Test if the duplicates are removed appropriately with 5 tower teams"""
        RandomGen.set_seed(7337)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("Jun Yu", 2, team_size=4, criterion=Criterion.DEF))
        bt.generate_teams(5)
        RandomGen.set_seed(35727188)

        # The team numbers of the tower before removing the duplicates  
        before_duplicate = [[1, 0, 5, 0, 0],
                            [0, 0, 1, 2, 0],
                            [0, 3, 0, 0, 0],
                            [2, 1, 0, 1, 0],
                            [0, 0, 4, 1, 0]]
        
        # The team numbers of the tower after removing the duplicates  
        # All the teams in the tower were duplicates
        after_duplicate = []

        for i in (range(len(bt.teams))):
            team = bt.teams.serve()
            self.assertEqual(team.get_team_numbers(), before_duplicate[i])
            bt.teams.append(team)
        
        it = iter(bt)
        it.avoid_duplicates()
        
        self.assertEqual(len(bt.teams), 0)