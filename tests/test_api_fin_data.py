# the code in this file is newly written to unit-test the code in 'fin_data.py'
# the whole coding process followed the three laws of test driven development

import unittest
import api_fin_data
import os

class TestAPIFinData(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(api_fin_data.APIFinData)

        get_fin_data=api_fin_data.APIFinData()
        self.assertIsNotNone(get_fin_data.stock_symbol_file)
        self.assertIsNotNone(get_fin_data.json_filename)
        self.assertIsNotNone(get_fin_data.get_symbol_from_csv)
        self.assertIsNotNone(get_fin_data.get_financial_data)
        self.assertIsNotNone(get_fin_data.append_to_json)
        self.assertIsNotNone(get_fin_data.read_from_pickle_binary_file)
        self.assertIsNotNone(get_fin_data.write_to_pickle_binary_file)
        self.assertIsNotNone(get_fin_data.get_nth_date)

    # test if functions return or output something
    def test_function_returns(self):
        get_fin_data=api_fin_data.APIFinData()

        # testing "get_symbol_from_csv()"
        self.assertIsNotNone(get_fin_data.get_symbol_from_csv('2020-01-01'))

        # testing "get_financial_data()"
        ## make request to external API
        symbol='MSFT'
        data_msft=get_fin_data.get_financial_data(symbol=symbol)
        self.assertIsNotNone(data_msft)

        symbol='ABC'
        data=get_fin_data.get_financial_data(symbol=symbol)
        self.assertIsNone(data)

        # testing "append_to_json()"
        test_json_path='JSON/test.json'
        get_fin_data.append_to_json({'content': 'test content'}, test_json_path)
        self.assertTrue(os.path.exists(test_json_path))
        os.remove(test_json_path)

        # testing "write_to_pickle_binary_file()"
        test_pickle_path='pickle/test.pickle'
        get_fin_data.write_to_pickle_binary_file(test_pickle_path, 'test data')
        self.assertTrue(os.path.exists(test_pickle_path))

        # testing "read_from_pickle_binary_file()"
        read_pickle=get_fin_data.read_from_pickle_binary_file(test_pickle_path)
        self.assertIsNotNone(read_pickle)
        self.assertEqual(str(read_pickle), 'test data')

        ## remove the test pickle file
        os.remove(test_pickle_path)

        # testing "get_nth_date()"
        self.assertIsNotNone(get_fin_data.get_nth_date(data_msft))
        self.assertIsNotNone(get_fin_data.get_nth_date(data_msft, n=0))

    # test if variables store correct type of data
    def test_var_type(self):
        get_fin_data=api_fin_data.APIFinData()
        self.assertEqual(str(type(get_fin_data.stock_symbol_file)), "<class 'str'>")
        self.assertEqual(str(type(get_fin_data.json_filename)), "<class 'str'>")

    # test if get_financial_data() works as expected
    def test_get_financial_data(self):
        get_fin_data=api_fin_data.APIFinData()
        # make request to external API
        symbol='MSFT'
        api_data=get_fin_data.get_financial_data(symbol=symbol)
        self.assertIsNotNone(api_data)
        # test if a pickle file was saved successfully, and test if the pickle can be read
        data=get_fin_data.read_from_pickle_binary_file('pickle/stock_data/' + symbol + '_max.pkl')
        self.assertIsNotNone(data)
        self.assertEqual(str(type(data)), "<class 'pandas.DataFrame'>")

        symbol='ABC'
        api_data=get_fin_data.get_financial_data(symbol=symbol)
        self.assertIsNone(api_data)
        # test if a pickle file was saved successfully, and test if the pickle can be read
        file_path='pickle/stock_data/' + symbol + '_max.pkl'
        self.assertFalse(os.path.exists(file_path))

    # test if all constituent stocks of S&P500 can be retrieved
    # the result will be stored to two csv files ('downloadable_stock_code.csv' and 'undownloadable_stock_code.csv')
    def test_all_sp500(self):
        get_fin_data=api_fin_data.APIFinData()
        # get all stock code
        symbols = get_fin_data.get_symbol_from_csv('2020-01-01')
        downloadable = []
        undownloadable = []
        for s in symbols:
            data=get_fin_data.get_financial_data(symbol=s)
            if data is None:
                undownloadable.append(s)
            else:
                downloadable.append(s)

        # at least the data from a stock of S&P500 can be downloaded
        self.assertGreater(len(downloadable), 0)

        # the no. of result equals the no. of symbols
        self.assertEqual(len(symbols), len(downloadable) + len(undownloadable))

        # check the list of downloadable and undownloadable symbols respectively
        downloadable_filename='CSV/downloadable_stock_code.csv'
        with open(downloadable_filename) as f:
            csv_content = f.read()
        for i in range(len(downloadable)):
            self.assertTrue(downloadable[i] in csv_content)

        undownloadable_filename='CSV/undownloadable_stock_code.csv'
        with open(undownloadable_filename) as f:
            csv_content = f.read()
        for i in range(len(undownloadable)):
            self.assertTrue(undownloadable[i] in csv_content)

        # check if lists created successfully
        self.assertTrue(os.path.exists(downloadable_filename))
        self.assertTrue(os.path.exists(undownloadable_filename))

