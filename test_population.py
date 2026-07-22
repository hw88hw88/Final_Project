import unittest
import population 

class TestPopulation(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(population.Population)

    # test if the population size can be correctly created
    def test_pop_length(self):
        self.assertEqual(len(population.Population(start_up_cash=100000, pop_size=5).strategies), 5)

unittest.main()