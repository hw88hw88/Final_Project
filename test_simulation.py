import unittest
import simulation
import strategy
import pandas as pd
import api_fin_data

class TestSimulation(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(simulation.Simulation)

        sim=simulation.Simulation(fin_start='2020-01-01', fin_end='2020-01-31', trading_fee=0.01)
        self.assertIsNotNone(sim.api)
        self.assertIsNotNone(sim.calculate_fin_indicator_for_stock)
        self.assertIsNotNone(sim.sorting_stocks)
        self.assertIsNotNone(sim.run_strategy)

    # test if functions return something
    def test_function_returns(self):
        sim=simulation.Simulation(fin_start='2020-01-01', fin_end='2020-01-31', trading_fee=0.01)
        st=strategy.Strategy(start_up_cash=100000)

        # testing "calculate_fin_indicator_for_stock()"
        df_score=sim.calculate_fin_indicator_for_stock(st=st, symbol='MSFT')
        self.assertIsNotNone(df_score)
        df_score2=sim.calculate_fin_indicator_for_stock(st=st, symbol='AAPL')
        self.assertIsNotNone(df_score2)

        # testing "sorting_stocks()"
        stocks_df=[df_score, df_score2]
        ### finding the 1st day in the data frame
        first_date=api_fin_data.APIFinData.get_nth_date(df_score, n=1)

        sorting_stocks=sim.sorting_stocks(date_timestamp=first_date, stocks_df=stocks_df, st=st)
        self.assertIsNotNone(sorting_stocks)

    # test if the functions return correct data type
    def test_function_return_type(self):
        sim=simulation.Simulation(fin_start='2020-01-01', fin_end='2020-01-31', trading_fee=0.01)
        st=strategy.Strategy(start_up_cash=100000)

        # testing "calculate_fin_indicator_for_stock()"
        df_score=sim.calculate_fin_indicator_for_stock(st=st, symbol='MSFT')
        self.assertEqual(str(type(df_score)), "<class 'pandas.DataFrame'>")

        # testing "sorting_stocks()"
        df_score2=sim.calculate_fin_indicator_for_stock(st=st, symbol='AAPL')
        stocks_df=[df_score, df_score2]
        ### finding the 1st day in the data frame
        first_date=api_fin_data.APIFinData.get_nth_date(df_score)

        sorted_stocks=sim.sorting_stocks(date_timestamp=first_date, stocks_df=stocks_df, st=st)
        self.assertEqual(str(type(sorted_stocks)), "<class 'list'>")

    # test if the returned value is correct
    def test_function_return_value(self):
        fin_start='2020-01-01'
        fin_end='2020-01-31'
        sim=simulation.Simulation(fin_start=fin_start, fin_end=fin_end, trading_fee=0.01)
        st=strategy.Strategy(start_up_cash=100000)

        # testing "calculate_fin_indicator_for_stock()"
        df_score=sim.calculate_fin_indicator_for_stock(st=st, symbol='MSFT')
        df_score_dict=df_score.to_dict()
        columns=list(df_score_dict.keys())
        key_time=list(df_score_dict[columns[0]].keys())
        ## The returned data frame should be within the specified period
        self.assertGreaterEqual(pd.Timestamp(key_time[0]), pd.Timestamp(fin_start))
        self.assertLessEqual(pd.Timestamp(key_time[-1]), pd.Timestamp(fin_end))

        ## check existance of new columns
        self.assertIsNotNone(df_score['rsi'])
        self.assertIsNotNone(df_score['ma_short'])
        self.assertIsNotNone(df_score['ma_long'])
        self.assertIsNotNone(df_score['signal_score'])
        self.assertIsNotNone(df_score['daily_returns'])

        ## check data type of new columns
        self.assertEqual(str(type(df_score['rsi'])), "<class 'pandas.Series'>")
        self.assertEqual(str(type(df_score['ma_short'])), "<class 'pandas.Series'>")
        self.assertEqual(str(type(df_score['ma_long'])), "<class 'pandas.Series'>")
        self.assertEqual(str(type(df_score['signal_score'])), "<class 'pandas.Series'>")
        self.assertEqual(str(type(df_score['daily_returns'])), "<class 'pandas.Series'>")

        # testing "sorting_stocks()"
        df_score2=sim.calculate_fin_indicator_for_stock(st=st, symbol='AAPL')
        stocks_df=[df_score, df_score2]
        ## finding the 1st day in the data frame
        first_date=api_fin_data.APIFinData.get_nth_date(df_score)

        sorted_stocks=sim.sorting_stocks(date_timestamp=first_date, stocks_df=stocks_df, st=st)
        ## testing the length of the returned value
        ### the no. of stock in this testing should be 2. They are 'AAPL' & 'MSFT'. st.gdict['max_num_of_stock'] can be more than 2.
        self.assertLessEqual(len(sorted_stocks), st.gdict['max_num_of_stock'])

    # test run_strategy()
    def test_run_strategy(self):
        sim=simulation.Simulation(fin_start='2020-01-01', fin_end='2020-12-31', trading_fee=0.01)
        start_up_cash=100000
        st=strategy.Strategy(start_up_cash=start_up_cash)

        sim.run_strategy(st=st)
        self.assertEqual(len(list(st.stocks.keys())), 0)
        self.assertNotEqual(st.total_value, start_up_cash)

        print('st.total_value= ', st.total_value)

unittest.main()
