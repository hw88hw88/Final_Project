import unittest
import chatbot
import file_mgt
import genome
import os
import strategy

class TestChatbot(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(chatbot.Chatbot)
        self.assertIsNotNone(chatbot.Chatbot.get_run_id)
        self.assertIsNotNone(chatbot.Chatbot.get_strategy)
        self.assertIsNotNone(chatbot.Chatbot.get_data)

    # test the get_strategy()
    def test_get_strategy(self):
        bot = chatbot.Chatbot()

        fm = file_mgt.FileMgt()
        # create a testing strategy
        g = genome.Genome()
        spec=g.get_gene_spec()
        
        test_gdict = g.get_gdict(
            gene=g.get_random_gene(gene_length=len(spec)),
            spec=spec
            )
        spec['run_id'] = str('unittest')

        # test file path
        test_run_id_file = 'CSV/unittest_run_id.csv'
        test_hyper_params_file = 'JSON/unittest_hyper_parameter.json'
        test_gdict_file = 'JSON/unittest_gdict.json'

        # create test files
        ## test_run_id file
        fm.write_csv(
            csv_file_path=test_run_id_file,
            to_csv_content='test_id'
        )

        ## test_hyper-parameters file
        fm.write_to_json(
            to_json_content={'num_of_generations': 50},
            filename=test_hyper_params_file
        )

        ## test gdict file
        fm.write_to_json(
            to_json_content=test_gdict,
            filename=test_gdict_file,
        )

        trained_strategy = bot.get_strategy(
            run_id_file_path=test_run_id_file,
            hyper_params_file_path=test_hyper_params_file,
            gdict_file_path=test_gdict_file,
        )
        self.assertEqual(trained_strategy.gdict, test_gdict)

        # remove test files
        os.remove(test_run_id_file)
        os.remove(test_hyper_params_file)
        os.remove(test_gdict_file)

    # test get_run_id()
    def test_get_run_id(self):
        bot = chatbot.Chatbot()
        fm = file_mgt.FileMgt()

        # write run_id to a test file
        run_id_file_path='CSV/unittest_run_id.csv'
        fm.write_csv(csv_file_path=run_id_file_path, to_csv_content='test')

        run_id = bot.get_run_id(num_of_run=0, run_id_file_path=run_id_file_path)

        # check the content of the run_id
        self.assertEqual(run_id, 'test')

        # remove test file
        os.remove(run_id_file_path)

    # test get_data()
    def test_get_data(self):
        bot = chatbot.Chatbot()
        st = strategy.Strategy()
        stocks_df = bot.get_data(
            trading_date='2023-01-31',
            st=st,
            trading_fee=0.01
            )

        self.assertIsNotNone(stocks_df)
        self.assertEqual(str(type(stocks_df)), "<class 'list'>")
        self.assertEqual(str(type(stocks_df[0])), "<class 'pandas.DataFrame'>")
        for df in stocks_df:
            self.assertEqual(len(df), 1)

    # test get_investment_portfolio()
    def test_get_investment_portfolio(self):
        bot = chatbot.Chatbot()
        st = strategy.Strategy()
        trading_date='2023-01-31'
        stocks_df = bot.get_data(
            trading_date=trading_date,
            st=st,
            trading_fee=0.01
            )

        portfolio = bot.get_investment_portfolio(
            st = st,
            stocks_df = stocks_df,
            trading_date=trading_date
        )

        self.assertIsNotNone(portfolio)
        print('portfolio= ', portfolio)
        self.assertEqual(str(type(portfolio)), "<class 'list'>")
