import unittest
import ga
import os
import population
import file_mgt

class TestGA(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(ga.GA)
        self.assertIsNotNone(ga.GA.metrics)
        self.assertIsNotNone(ga.GA.elitism)
        self.assertIsNotNone(ga.GA.run_ga)
        self.assertIsNotNone(ga.GA.initialise_logs)
        self.assertIsNotNone(ga.GA.close_ga_performance_file)

        the_ga=ga.GA(pool_size=1,
            start_up_cash=100000,
            trading_fee=0.01,
            pop_size=2,
            num_of_generations=2,
            point_mutate_rate=0.1, 
            point_mutate_amt=0.25,
            fin_start='2020-12-01',
            fin_end='2020-12-31',
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
            fin_start='2020-12-01',
            fin_end='2020-12-31',
        )
        the_ga.initialise_logs()
        self.assertTrue(os.path.exists(the_ga.hyper_parameter_filename))
        self.assertTrue(os.path.exists(the_ga.gene_spec_filename))
        self.assertFalse(os.path.exists(the_ga.ga_performance_filename))

        os.remove(the_ga.hyper_parameter_filename)
        os.remove(the_ga.gene_spec_filename)

    # test metrics()
    def test_metrics(self):
        start_up_cash=100000
        pop_size=2

        the_ga=ga.GA(pool_size=1,
            start_up_cash=start_up_cash,
            trading_fee=0.01,
            pop_size=pop_size,
            num_of_generations=2,
            point_mutate_rate=0.1, 
            point_mutate_amt=0.25,
            fin_start='2020-12-01',
            fin_end='2020-12-31',
        )

        the_ga.run_ga()

        self.assertIsNotNone(the_ga.ga_performance_file_content)
        self.assertEqual(str(type(the_ga.ga_performance_file_content)), "<class 'str'>")
        self.assertGreater(len(the_ga.ga_performance_file_content), 5)

    # test elitism()
    def test_elitism(self):
        start_up_cash = 100000
        pop_size = 4
        num_of_elite = 2

        num_of_generations=2

        # checking generation 0
        generation=0

        the_ga=ga.GA(pool_size=1,
            start_up_cash=start_up_cash,
            trading_fee=0.01,
            pop_size=pop_size,
            num_of_generations=num_of_generations,
            point_mutate_rate=0.1, 
            point_mutate_amt=0.25,
            fin_start='2020-12-01',
            fin_end='2020-12-31',
            num_of_elite = num_of_elite,
        )
        the_ga.initialise_logs()
        pop = population.Population(start_up_cash=start_up_cash, pop_size=pop_size)

        top_n_st, rewards = the_ga.elitism(
            pop=pop,
            generation=generation
        )

        # check returned value
        self.assertIsNotNone(top_n_st)
        self.assertIsNotNone(rewards)

        self.assertEqual(str(type(top_n_st)), "<class 'list'>")
        self.assertEqual(len(top_n_st), num_of_elite)

        self.assertEqual(str(type(rewards)), "<class 'list'>")
        self.assertEqual(len(rewards), pop_size)

        # check saved files
        self.assertTrue(os.path.exists(the_ga.elite_csv_filepath + '/elite_gene_gen' + str(generation) + '_' + str(num_of_elite - 1) + '.csv'))

        self.assertTrue(os.path.exists(the_ga.elite_json_filepath + '/elite_gdict_gen' + str(generation) + '_' + str(num_of_elite - 1) + '.json'))

        # remove test files
        os.remove(the_ga.elite_csv_filepath + '/elite_gene_gen' + str(generation) + '_' + str(num_of_elite - 1) + '.csv')
        os.remove(the_ga.elite_json_filepath + '/elite_gdict_gen' + str(generation) + '_' + str(num_of_elite - 1) + '.json')

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
            fin_start='2020-12-01',
            fin_end='2020-12-31',
        )

        the_ga.run_ga()

        self.assertIsNotNone(the_ga.ga_performance_filename)
        self.assertTrue(os.path.exists(the_ga.ga_performance_filename))
        self.assertTrue(os.path.exists(the_ga.hyper_parameter_filename))
        self.assertTrue(os.path.exists(the_ga.gene_spec_filename))

        os.remove(the_ga.ga_performance_filename)
        os.remove(the_ga.hyper_parameter_filename)
        os.remove(the_ga.gene_spec_filename)

    # test initialise_logs()
    def test_initialise_logs(self):
        test_content = {'test content': 'test content'}
        filepath = 'JSON/test.json'
        file_mgt.FileMgt.write_to_json(to_json_content=test_content, filename=filepath)

        start_up_cash=100000
        pop_size=3

        the_ga=ga.GA(pool_size=1,
            start_up_cash=start_up_cash,
            trading_fee=0.01,
            pop_size=pop_size,
            num_of_generations=2,
            point_mutate_rate=0.1, 
            point_mutate_amt=0.25,
            fin_start='2020-12-01',
            fin_end='2020-12-31',
        )

        # run initialise_log()
        the_ga.initialise_logs()
        self.assertTrue(os.path.exists(the_ga.hyper_parameter_filename))
        self.assertTrue(os.path.exists(the_ga.gene_spec_filename))

        # remove test files
        os.remove(filepath)
        os.remove(the_ga.hyper_parameter_filename)
        os.remove(the_ga.gene_spec_filename)

    # test close_ga_performance_file()
    def test_close_ga_performance_file(self):
        # initialise the test
        the_ga=ga.GA(
            pool_size=1,
            start_up_cash=100000,
            trading_fee=0.01,
            pop_size=2,
            num_of_generations=2,
            point_mutate_rate=0.1, 
            point_mutate_amt=0.25,
            fin_start='2020-12-01',
            fin_end='2020-12-31',
        )

        the_ga.close_ga_performance_file()

        self.assertTrue(os.path.exists(the_ga.ga_performance_filename))

        # remove test file
        os.remove(the_ga.ga_performance_filename)

    # tear down
    def test_tear_down(self):
        # remove files in 'JSON/unittest_fittest'
        files = file_mgt.FileMgt.list_files_in_directory('JSON/unittest_fittest')
        # remove files in 'CSV/unittest_fittest'
        files.extend(file_mgt.FileMgt.list_files_in_directory('CSV/unittest_fittest'))
        for f in files:
            os.remove(f)
            self.assertFalse(os.path.exists(f))
