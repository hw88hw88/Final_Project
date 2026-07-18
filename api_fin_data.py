import os
import pickle
import time
import json
import yfinance as yf
import pandas as pd

class APIFinData:
    def __init__(self):
        # store the file path of stock code
        self.stock_symbol_file='CSV/stock_code.csv'
        # store the file path of the stock code which the data of the stock was downloadble
        self.stock_symbol_file_downloadable='CSV/downloadable_stock_code.csv'
        # store the log file path
        self.json_filename='JSON/api_log.json'

    # this function retrieve the symbols of constituent stocks of the Standard & Poor’s 500 (S&P500) on a specified date from a csv file
    def get_symbol_from_csv(self):
        symbol=[]
        # Some stock code are invalid
        # During the testing in 'test_all_sp500()' in test_fin_data.py, the stock code was split into 2 lists, i.e. downloadable and undownloadable. If there is a list of downloadable stocks, the list will be used. Otherwise, the original list of stock will be used.
        if os.path.exists(self.stock_symbol_file_downloadable):
            filename=self.stock_symbol_file_downloadable
        else:
            filename=self.stock_symbol_file
        with open(filename) as f:
            csv_str = f.read()
            lines = csv_str.split('\n')
            for line in lines:
                tickers = line.split(',')
                for ticker in tickers:
                    if ticker != '':
                        symbol.append(str(ticker))
        return symbol

    # get the financial data from external API
    ## input:
    ### symbol: the stock code e.g. "MSFT", "MU"
    ## output:
    ### raw_data: the dataframe from the external API
    def get_financial_data(self, symbol):
        # store the raw data in pickle file for later retrieval
        pickle_filename='pickle/stock_data/'+symbol+'_max.pkl'
        # store the data frame of raw data in csv file, because this is human readable form
        df_csv_filename='CSV/stock_data/'+symbol+'_max.csv'

        # # check if the data was saved in files
        if not os.path.exists(pickle_filename):
            # download the data from external source if not exist
            raw_data = yf.download(symbol, period='max', auto_adjust=True)
            # wait to avoid abuse the API
            time.sleep(1)

            # check if the raw data is empty
            # For an empty data frame from yfinance, there are 7 elements
            if raw_data is None or int(raw_data.size) < 1:
                return None
            if symbol=='ABC':
                print('size= ', raw_data.size)

            # convert the raw data to pickle format and
            # save to pickle file
            self.write_to_pickle_binary_file(filename=pickle_filename, data=raw_data)
            # save to human readable format, CSV file
            raw_data.to_csv(df_csv_filename)
            # saving the log of the requests to external API        
            self.append_to_json(to_json_content={'symbol': symbol} , filename=self.json_filename)
        else:
            # load data from file
            raw_data=self.read_from_pickle_binary_file(filename=pickle_filename)
        return raw_data
    
    # finding the n (default: the first, if n is None) timestamp in the pandas frame from yfinance
    # input: 
    ## 1. df: data frame storing a single stock
    ## 2. n: (int) the Nth day in the data frame
    # output: the n timestamp in the input data frame, in the format of pandas timestamp
    @staticmethod
    def get_nth_date(df, n=None):
        # finding the 1st day in the data frame
        df_dict=df.to_dict()
        ## the keys of the dict() are the name of columns
        df_dict_columns=list(df_dict.keys())
        ## the keys are the time stamp of each row
        df_dict_key_time=list(df_dict[df_dict_columns[0]].keys())
        if n is None:
            ## the first timestamp
            return pd.Timestamp(df_dict_key_time[0])
        else:
            ## the Nth timestamp
            if abs(n) < len(df_dict_key_time):
                return pd.Timestamp(df_dict_key_time[n])
            else:
                # if abs(n) is large than the number of rows in the data frame
                # return the last date in the data frame
                return pd.Timestamp(df_dict_key_time[-1])

    # converting data the json format and save to a file (append the content)
    @staticmethod
    def append_to_json(to_json_content, filename):
        content = json.dumps(to_json_content)
        with open(filename, 'a') as f:
            f.write(content)

    # reading pickle from binary file
    @staticmethod
    def read_from_pickle_binary_file(filename):
        with open(filename, 'rb') as f:
            data = f.read()
        return pickle.loads(data)

    # writing pickle to binary file
    @staticmethod
    def write_to_pickle_binary_file(filename, data):
        pickled_data=pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
        with open(filename, 'wb') as f:
            f.write(pickled_data)

