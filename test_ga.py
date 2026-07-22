import unittest
import ga
import os
import population
import file_mgt

class TestGA(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(ga.GA)
        self.assertIsNotNone(ga.GA.matrics)
        self.assertIsNotNone(ga.GA.elitism)
        self.assertIsNotNone(ga.GA.run_ga)

        the_ga=ga.GA(pool_size=1,
            start_up_cash=100000,
            trading_fee=0.01,
            pop_size=2,
            num_of_generations=2,
            point_mutate_rate=0.1, 
            point_mutate_amt=0.25,
            fin_start='2020-01-01',
            fin_end='2020-01-31',
        )
        self.assertIsNotNone(the_ga.fin_start)
        self.assertIsNotNone(the_ga.fin_end)
        self.assertIsNotNone(the_ga.start_up_cash)
        self.assertIsNotNone(the_ga.trading_fee)
        self.assertIsNotNone(the_ga.gene_spec_filename)
        self.assertIsNotNone(the_ga.ga_performance_filename)
        self.assertIsNotNone(the_ga.hyper_parameter_filename)

        self.assertIsNotNone(the_ga.num_of_generations)
        self.assertIsNotNone(the_ga.point_mutate_rate)
        self.assertIsNotNone(the_ga.point_mutate_amt)

    # test files can be written successfully by __init__()
    def test_save_to_json_content(self):
        the_ga=ga.GA(pool_size=1, 
            start_up_cash=100000,
            trading_fee=0.01,
            pop_size=2,
            num_of_generations=2,
            point_mutate_rate=0.1, 
            point_mutate_amt=0.25,
            fin_start='2020-01-01',
            fin_end='2020-01-31',
        )
        self.assertTrue(os.path.exists(the_ga.hyper_parameter_filename))
        self.assertTrue(os.path.exists(the_ga.gene_spec_filename))
        self.assertFalse(os.path.exists(the_ga.ga_performance_filename))

        os.remove(the_ga.hyper_parameter_filename)
        os.remove(the_ga.gene_spec_filename)

    # test matrics()
    def test_matrics(self):
        start_up_cash=100000
        pop_size=2

        the_ga=ga.GA(pool_size=1,
            start_up_cash=start_up_cash,
            trading_fee=0.01,
            pop_size=pop_size,
            num_of_generations=2,
            point_mutate_rate=0.1, 
            point_mutate_amt=0.25,
            fin_start='2020-01-01',
            fin_end='2020-01-31',
        )
        pop = population.Population(start_up_cash=start_up_cash, pop_size=pop_size)

        for p in range(pop_size):
            pop.strategies[p].age +=1
            self.assertNotEqual(pop.strategies[p].age, 0)

        the_ga.fittest_st = pop.strategies
        the_ga.matrics(generation=1)

        self.assertIsNotNone(the_ga.ga_performance_file_content)
        self.assertEqual(str(type(the_ga.ga_performance_file_content)), "<class 'str'>")
        self.assertGreater(len(the_ga.ga_performance_file_content), 5)

    # test elitism()
    def test_elitism(self):
        start_up_cash=100000
        pop_size=2

        the_ga=ga.GA(pool_size=1,
            start_up_cash=start_up_cash,
            trading_fee=0.01,
            pop_size=pop_size,
            num_of_generations=2,
            point_mutate_rate=0.1, 
            point_mutate_amt=0.25,
            fin_start='2020-01-01',
            fin_end='2020-01-31',
        )
        pop = population.Population(start_up_cash=start_up_cash, pop_size=pop_size)
        the_ga.fittest_st = pop.strategies

        the_ga.elitism(
            pop=pop,
            generation=1
        )

        self.assertIsNotNone(the_ga.fittest_st)
        self.assertEqual(str(type(the_ga.fittest_st)), "<class 'list'>")
        self.assertGreater(len(the_ga.fittest_st), 0)

    # test run_ga()
    def test_run_ga(self):
        start_up_cash=100000
        pop_size=3

        the_ga=ga.GA(pool_size=1,
            start_up_cash=start_up_cash,
            trading_fee=0.01,
            pop_size=pop_size,
            num_of_generations=2,
            point_mutate_rate=0.1, 
            point_mutate_amt=0.25,
            fin_start='2020-01-01',
            fin_end='2020-01-31',
        )

        the_ga.run_ga()

        self.assertIsNotNone(the_ga.ga_performance_filename)
        self.assertTrue(os.path.exists(the_ga.ga_performance_filename))
        self.assertTrue(os.path.exists(the_ga.hyper_parameter_filename))
        self.assertTrue(os.path.exists(the_ga.gene_spec_filename))

        files = file_mgt.FileMgt.list_files_in_directory('JSON')
        for file in files:
            os.remove(file)

############################################################ add
unittest.main()
