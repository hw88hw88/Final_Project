import unittest
import chatbot
import file_mgt
import genome
import os
import strategy
import json
import re

class TestChatbot(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(chatbot.Chatbot)
        self.assertIsNotNone(chatbot.Chatbot.get_run_id)
        self.assertIsNotNone(chatbot.Chatbot.get_strategy)
        self.assertIsNotNone(chatbot.Chatbot.get_data)
        self.assertIsNotNone(chatbot.Chatbot.get_investment_portfolio)
        self.assertIsNotNone(chatbot.Chatbot.apply_strategy)
        self.assertIsNotNone(chatbot.Chatbot.generate_advice)
        self.assertIsNotNone(chatbot.Chatbot.generate_custom_response)
        self.assertIsNotNone(chatbot.Chatbot.identify_user_input)

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
        test_gdict['run_id'] = str('unittest')

        # test file path
        test_hyper_params_file = 'JSON/unittest_hyper_parameter.json'
        test_gdict_file = 'JSON/unittest_gdict.json'

        # create test files
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

        test_run_id = 'unittest_id'

        trained_strategy, gdict = bot.get_strategy(
            run_id=test_run_id,
            hyper_params_file_path=test_hyper_params_file,
            gdict_file_path=test_gdict_file,
        )
        self.assertEqual(trained_strategy.gdict, test_gdict)

        # remove test files
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

        fm.write_csv(csv_file_path=run_id_file_path, to_csv_content='test, test2, test3,')
        run_id = bot.get_run_id(num_of_run=1, run_id_file_path=run_id_file_path)
        # check the content of the run_id
        self.assertEqual(run_id, 'test2')

        run_id = bot.get_run_id(num_of_run=2, run_id_file_path=run_id_file_path)
        # check the content of the run_id
        self.assertEqual(run_id, 'test3')

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
        self.assertEqual(str(type(portfolio)), "<class 'list'>")

    # test apply_strategy()
    def test_apply_strategy(self):
        # create testing run_id
        test_run_id = 'unittest'
        bot = chatbot.Chatbot()
        fm = file_mgt.FileMgt()

        # write run_id to a test file
        run_id_file_path='CSV/unittest_run_id.csv'
        fm.write_csv(csv_file_path=run_id_file_path, to_csv_content=test_run_id)

        # create a testing strategy
        g = genome.Genome()
        spec=g.get_gene_spec()
        
        test_gdict = g.get_gdict(
            gene=g.get_random_gene(gene_length=len(spec)),
            spec=spec
            )
        spec['run_id'] = str(test_run_id)
        test_gdict['run_id'] = str(test_run_id)

        # test file path
        test_hyper_params_file = 'JSON/unittest_hyper_parameter.json'
        test_gdict_file = 'JSON/unittest_gdict.json'

        # create test files
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

        #  test apply_strategy()
        portfolio, portfolio_dict, st, gdict = bot.apply_strategy(
            trading_date='2023-01-31',
            num_of_run = 0,
            trading_fee = 0.01,
            run_id_file_path = run_id_file_path,
            hyper_params_file_path=test_hyper_params_file,
            gdict_file_path=test_gdict_file
        )

        self.assertIsNotNone(portfolio)
        self.assertIsNotNone(portfolio_dict)
        self.assertIsNotNone(st)
        self.assertIsNotNone(gdict)

        self.assertEqual(test_gdict['run_id'], gdict['run_id'])
        self.assertGreater(len(list(portfolio_dict.keys())), 0)
        self.assertEqual(gdict, st.gdict)

    # test generate_advice()
    def test_generate_advice(self):
        trading_date='2023-01-31'
        # create testing run_id
        test_run_id = 'unittest'
        bot = chatbot.Chatbot()
        fm = file_mgt.FileMgt()

        # write run_id to a test file
        run_id_file_path='CSV/unittest_run_id.csv'
        fm.write_csv(csv_file_path=run_id_file_path, to_csv_content=test_run_id)

        # create a testing strategy
        g = genome.Genome()
        spec=g.get_gene_spec()
        
        test_gdict = g.get_gdict(
            gene=g.get_random_gene(gene_length=len(spec)),
            spec=spec
            )
        spec['run_id'] = str(test_run_id)
        test_gdict['run_id'] = str(test_run_id)

        # test file path
        test_hyper_params_file = 'JSON/unittest_hyper_parameter.json'
        test_gdict_file = 'JSON/unittest_gdict.json'

        # create test files
        ## test_hyper-parameters file
        fm.write_to_json(
            to_json_content={'num_of_generations': 50},
            filename=test_hyper_params_file
        )

        ## create gdict file
        fm.write_to_json(
            to_json_content=test_gdict,
            filename=test_gdict_file,
        )

        #  run apply_strategy() to get the input arguments
        portfolio, portfolio_dict, st, gdict = bot.apply_strategy(
            trading_date=trading_date,
            num_of_run = 0,
            trading_fee = 0.01,
            run_id_file_path = run_id_file_path,
            hyper_params_file_path=test_hyper_params_file,
            gdict_file_path=test_gdict_file
        )

        chatbot_response = bot.generate_advice(
            portfolio=portfolio,
            portfolio_dict=portfolio_dict,
            trading_date=trading_date
        )

        self.assertIsNotNone(chatbot_response)
        self.assertGreater(len(chatbot_response), 0)
        self.assertEqual(str(type(chatbot_response)), "<class 'str'>")
        print(chatbot_response)

    # test identify_user_input()
    def test_identify_user_input(self):
        bot = chatbot.Chatbot()
        user_prompt=[
            "I would like to invest my money. Please give me advice.",
            "Please explain your recommendations.",
            "I'm bored.",
            "How to calculate 1+1?",
            "My birthday is on 1 January 2030",
            "Tell me your recommendations yesterday.",
            "I prefer high return but low risk.",
            ]

        for user_p in user_prompt:
            raw_output = bot.identify_user_input(user_prompt=user_p)
            response = raw_output
            self.assertIsNotNone(response)
            self.assertEqual(str(type(response)), "<class 'dict'>")
            self.assertIsNone(response.get('error'))

    # test generate_custom_response()
    def test_generate_custom_response(self):
        pass

