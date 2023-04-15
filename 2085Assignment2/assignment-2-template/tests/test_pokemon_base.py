from random_gen import RandomGen
from pokemon_base import PokemonBase, PokeType, StatusEffect
from pokemon import Blastoise, Bulbasaur, Charmander, Eevee, Gastly, Gengar, Haunter, Squirtle, Venusaur
from tests.base_test import BaseTest

class TestPokemonBase(BaseTest):

    def test_cannot_init(self):
        """Tests that we cannot initialise PokemonBase, and that it raises the correct error."""
        self.assertRaises(TypeError, lambda: PokemonBase(30, PokeType.FIRE))

    def test_level(self):
        e = Eevee()
        self.assertEqual(e.get_level(), 1)
        e.level_up()
        self.assertEqual(e.get_level(), 2)
    
    def test_hp(self):
        e = Eevee()
        self.assertEqual(e.get_hp(), 10)
        e.lose_hp(4)
        self.assertEqual(e.get_hp(), 6)
        e.heal()
        self.assertEqual(e.get_hp(), 10)

    def test_status(self):
        RandomGen.set_seed(0)
        e1 = Eevee()
        e2 = Eevee()
        e1.attack(e2)
        # e2 now is confused.
        e2.attack(e1)
        # e2 takes damage in confusion.
        self.assertEqual(e1.get_hp(), 10)

    def test_evolution(self):
        g = Gastly()
        self.assertEqual(g.can_evolve(), True)
        self.assertEqual(g.should_evolve(), True)
        new_g = g.get_evolved_version()
        self.assertIsInstance(new_g, Haunter)
        
    ###########################################################
    ################ Personal Designed Tests ##################
    
    def test_is_fainted(self):
        """ Test to check if a pokemon is fainted after losing the correct amount of damage"""
        g = Gastly() # hp = 6

        self.assertEqual(g.get_hp(), 6)

        g.lose_hp(5)
        self.assertEqual(g.get_hp(), 1)
        g.level_up()
        self.assertEqual(g.get_hp(), 2)
        g.heal()
        self.assertEqual(g.get_hp(), 7)

        g.lose_hp(8)
        self.assertEqual(g.is_fainted(), True)

    def test_attack(self):
        """ Test for the attack feature of the pokemon base class.
        Pokemons must attack each other dealing the relevant damage accoringly.
        """
        RandomGen.set_seed(10)

        c = Charmander()
        b = Bulbasaur()
        s = Squirtle()
        g = Gastly()

        c.attack(s)
        self.assertEqual(s.get_hp(), 10)
        self.assertEqual(s.get_status_effect(), StatusEffect.BURN)

        c.attack(b)
        self.assertEqual(b.get_hp(), -1)
        self.assertEqual(b.get_status_effect(), StatusEffect.NONE)

        g.attack(c)
        self.assertEqual(c.get_hp(), 4)
        self.assertEqual(c.get_status_effect(), StatusEffect.NONE)


    def test_multiplier(self):
        """ Test the correct effective multiplier based on the pokemon's type"""
        b = Bulbasaur()
        c = Charmander()
        s = Squirtle()
        e = Eevee()
        g  = Gastly()

        self.assertEqual(b.get_effective_multiplier(c), 0.5)
        self.assertEqual(c.get_effective_multiplier(b), 2)
        self.assertEqual(s.get_effective_multiplier(c), 2)
        self.assertEqual(b.get_effective_multiplier(s), 2)
        self.assertEqual(c.get_effective_multiplier(s), 0.5)
        self.assertEqual(e.get_effective_multiplier(g), 0)
        self.assertEqual(e.get_effective_multiplier(c), 1.25)

    def test_status(self):
        """ Test that the correct status is chosen to be inflicted based
        on the pokemon's types
        """
        b = Bulbasaur()
        c = Charmander()
        s = Squirtle()
        e = Eevee()
        g  = Gastly()

        self.assertEqual(b.get_inflict_status(), StatusEffect.POISON)
        self.assertEqual(c.get_inflict_status(), StatusEffect.BURN)
        self.assertEqual(s.get_inflict_status(), StatusEffect.PARALYSIS)
        self.assertEqual(e.get_inflict_status(), StatusEffect.CONFUSTION)
        self.assertEqual(g.get_inflict_status(), StatusEffect.SLEEP)
    
    def test_pokemon_str(self):
        """Test the pokemon base class magic str method"""
        h  = Haunter()
        g = Gengar()
        b = Blastoise()

        h.level_up()
        g.level_up()
        g.level_up()

        self.assertEqual(str(h), "LV. 2 Haunter: 10 HP")
        self.assertEqual(str(g), "LV. 5 Gengar: 14 HP")
        self.assertEqual(str(b), "LV. 3 Blastoise: 21 HP")


