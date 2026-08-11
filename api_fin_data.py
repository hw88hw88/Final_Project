import os
import pickle
import time
import json
import file_mgt
import yfinance as yf
import pandas as pd

class APIFinData:
    def __init__(self):
        # store the file path of stock code
        self.stock_symbol_file='CSV/S&P 500 Historical Components & Changes (Updated).csv'
        # store the file path of the stock code which the data of the stock was downloadble
        self.stock_symbol_file_downloadable='CSV/downloadable_stock_code.csv'

    # this function retrieve the symbols of constituent stocks of the Standard & Poor’s 500 (S&P500) on a specified date from a csv file
    # input:
    # 1. fin_start: the start date of the financial period (This is the date to determine the list of stocks. The trading date on or after the <fin_start> will be used)
    # output:
    # 1. a list of symbols
    def get_symbol_from_csv(self, fin_start):
        symbol=[]
        # using the list of symbols of S&P500 stocks from github
        ## Reference: <https://github.com/fja05680/sp500/blob/master/S%26P%20500%20Historical%20Components%20%26%20Changes%20(Updated).csv>
        filename=self.stock_symbol_file
        with open(filename) as f:
            csv_str = f.read()
        lines = csv_str.split('\n')
        for line in range(len(lines)):
            # the first line is the heading
            if line == 0:
                continue
            # remove the character double quotation mark ' " '
            lines[line] = lines[line].replace('"', '')
            # remove the character space ' '
            lines[line] = lines[line].strip()
            # split the line of content
            tickers = lines[line].split(',')
            # tickers[0] is the date of the S&P500 components
            # skip the line of symbols before the start date of the financial period
            if (pd.Timestamp(tickers[0]) < pd.Timestamp(fin_start) and 
                line < len(lines) - 1):
                continue
            # split the line of content
            ## the [line - 1] below means using the tickers just before the start of the financial period
            tickers = lines[line - 1].split(',')
            ## if the financial period <fin_start> begins after the last date on the list, use the symbols of the last date on the list
            if line == len(lines) - 1:
                tickers = lines[line].split(',')
            # return the first line of raw data on or after financial period
            for ticker in range(len(tickers)):
                # skip the date element
                if ticker == 0:
                    continue
                if tickers[ticker] != '':
                    symbol.append(str(tickers[ticker]))
            # return the first line of raw data on or after financial period
            return symbol

    # get the financial data from external API
    ## input:
    ### symbol: the stock code e.g. "MSFT", "MU"
    ## output:
    ### raw_data: the dataframe from the external API
    def get_financial_data(self, symbol):
        # check if the symbol has been tried but not downloadable
        ## reduce the number of requests made to the API
        undownloadable_filename='CSV/undownloadable_stock_code.csv'
        fm = file_mgt.FileMgt()
        if fm.check_file_exist(undownloadable_filename):
            undownloadable_symbols = fm.read_from_csv(undownloadable_filename)
            if symbol in undownloadable_symbols:
                # return None, if tried downloading but unsuccessful
                return None

        # store the raw data in pickle file for later retrieval
        pickle_filename='pickle/stock_data/'+symbol+'_max.pkl'
        # store the data frame of raw data in csv file, because this is human readable form
        df_csv_filename='CSV/stock_data/'+symbol+'_max.csv'

        # check if the folder exists for storing stock data in pickle
        if not os.path.exists('pickle'):
            os.mkdir('pickle')
        if not os.path.exists('pickle/stock_data'):
            os.mkdir('pickle/stock_data')

        # check if the folder exists for storing stock data in CSV
        if not os.path.exists('CSV'):
            os.mkdir('CSV')
        if not os.path.exists('CSV/stock_data'):
            os.mkdir('CSV/stock_data')

        # check if the folder exists for storing stock data in JSON
        if not os.path.exists('JSON'):
            os.mkdir('JSON')

        ## check if the data was saved in files to reduce the number of requests made to API and save time
        if not os.path.exists(pickle_filename):
            # download the data from external source if not exist
            raw_data = yf.download(symbol, period='max', auto_adjust=True)
            # wait to avoid abuse the API
            time.sleep(1)

            # check if the raw data is empty
            # record downloadable and undownloadable symbols in CSV files
            downloadable_filename='CSV/downloadable_stock_code.csv'
            if raw_data is None or int(raw_data.size) < 1:
                if fm.check_file_exist(undownloadable_filename):
                    undownloadable_symbols = fm.read_from_csv(undownloadable_filename)
                else:
                    undownloadable_symbols = []
                if symbol not in undownloadable_symbols:
                    undownloadable_symbols.append(symbol)
                    to_csv_str = ''
                    for sym in undownloadable_symbols:
                        to_csv_str += str(sym) + ','
                    fm.write_csv(
                        csv_file_path=undownloadable_filename,
                        to_csv_content=to_csv_str,
                    )
                return None
            if fm.check_file_exist(downloadable_filename):
                downloadable_symbols = fm.read_from_csv(downloadable_filename)
            else:
                downloadable_symbols = []
            if symbol not in downloadable_symbols:
                downloadable_symbols.append(symbol)
                to_csv_str = ''
                for sym in downloadable_symbols:
                    to_csv_str += str(sym) + ','
                fm.write_csv(
                    csv_file_path=downloadable_filename,
                    to_csv_content=to_csv_str,
                )

            # convert the raw data to pickle format and
            # save to pickle file
            self.write_to_pickle_binary_file(filename=pickle_filename, data=raw_data)
            # save to human readable format, CSV file
            raw_data.to_csv(df_csv_filename)

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

