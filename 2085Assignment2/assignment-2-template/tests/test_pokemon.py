from pokemon import Blastoise, Bulbasaur, Charizard, Charmander, Eevee, Gastly, Gengar, Haunter, Squirtle, Venusaur
from pokemon_base import StatusEffect
from tests.base_test import BaseTest

class TestPokemon(BaseTest):

    def test_venusaur_stats(self):
        v = Venusaur()
        self.assertEqual(v.get_hp(), 21)
        self.assertEqual(v.get_level(), 2)
        self.assertEqual(v.get_attack_damage(), 5)
        self.assertEqual(v.get_speed(), 4)
        self.assertEqual(v.get_defence(), 10)
        v.level_up()
        v.level_up()
        v.level_up()
        self.assertEqual(v.get_hp(), 22)
        self.assertEqual(v.get_level(), 5)
        self.assertEqual(v.get_attack_damage(), 5)
        self.assertEqual(v.get_speed(), 5)
        self.assertEqual(v.get_defence(), 10)
        v.lose_hp(5)

        self.assertEqual(str(v), "LV. 5 Venusaur: 17 HP")
    
    ###########################################################
    ################ Personal Designed Tests ##################
    
    def test_pokemon_speed(self):
        """ Test the expected speed stat of three pokemons"""

        C = Charizard()
        b = Blastoise()
        c = Charmander()

        c.level_up()
        self.assertEqual(c.get_speed(), 9)

        C.level_up()
        C.level_up()
        self.assertEqual(C.get_speed(), 14)

        b.level_up()
        self.assertEqual(b.get_speed(), 10)
    
    def test_pokemon_attack(self):
        """ Test the expected attack stat of three pokemons"""

        s = Squirtle()
        g = Gastly()
        h = Haunter()

        s.level_up()
        self.assertEqual(s.get_attack_damage(), 5)

        g.level_up()
        self.assertEqual(g.get_attack_damage(), 4)

        h.level_up()
        h.level_up()
        self.assertEqual(h.get_attack_damage(), 8)

    def test_pokemon_defence_pts(self):
        """ Test the expected defence points of three pokemon"""

        g = Gengar()
        e = Eevee()
        b = Bulbasaur()

        g.level_up()
        self.assertEqual(g.get_defence(), 3)

        e.level_up()
        self.assertEqual(e.get_defence(), 6)

        b.level_up()
        self.assertEqual(b.get_defence(), 5)
    
    def test_pokemon_evolution(self):
        """ Test the evolution of pokemon and test that after evolution the 
        evolved pokemon have the same status effect as their pre evolution.
        """
        
        c = Charmander()
        b = Bulbasaur()
        b.set_status_effect(StatusEffect.BURN)

        self.assertEqual(c.can_evolve(), True)
        self.assertEqual(b.can_evolve(), True)

        self.assertEqual(c.should_evolve(), False)
        c.level_up()
        c.level_up()
        self.assertEqual(c.should_evolve(), True)

        c = c.get_evolved_version()

        self.assertIsInstance(c, Charizard)

        self.assertEqual(b.should_evolve(), False)
        b.level_up()
        self.assertEqual(b.should_evolve(), True)

        b = b.get_evolved_version()

        self.assertIsInstance(b, Venusaur)
        self.assertEqual(b.get_status_effect(), StatusEffect.BURN)


    def test_pokemon_defend_and_name(self):
        """ Test the defend logic and mechanism for the three pokemon's and
        test their get name methods.
        """

        e = Eevee()
        c = Charizard()
        b = Blastoise()
        damage = 14

        self.assertEqual(e.defend(damage), 14)
        self.assertEqual(c.defend(damage), 28)
        self.assertEqual(b.defend(damage), 7)

        self.assertEqual(e.get_poke_name(), "Eevee")
        self.assertEqual(c.get_poke_name(), "Charizard")
        self.assertEqual(b.get_poke_name(), "Blastoise")
    
    def test_level_up(self):
        """ Test that leveling up the pokemon still obeys the difference in hp"""

        c = Charmander() # hp = 9

        c.lose_hp(5)

        self.assertEqual(c.get_hp(), 4)
        c.level_up()
        c.level_up()
        c.level_up()

        self.assertEqual(c.get_level(), 4)

        self.assertEqual(c.get_hp(), 7)


    




        

