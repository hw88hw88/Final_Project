import api_fin_data
import pandas as pd
import numpy as np

class Simulation:
    def __init__(self, fin_start, fin_end):
        self.api=api_fin_data.APIFinData()
        self.fin_start=fin_start
        self.fin_end=fin_end

    # calculate the financial indicators for stock
    ## input:
    ### 1. st: strategy
    ### 2. symbol: the stock code
    ## output:
    ### 1. pandas data frame storing the financial data and indicators of the stock
    def calculate_fin_indicator_for_stock(self, st, symbol):
        # retrieve the data from API or saved file
        raw_data=self.api.get_financial_data(symbol=symbol)

        # retrieve the data within the period
        pd_start=pd.Timestamp(self.fin_start)
        pd_end=pd.Timestamp(self.fin_end)

        # data 40 days before the start of the period for calculating financial indicators
        data_1mo_before_start=raw_data.loc[(raw_data.index <= pd_start)].tail(40)
        data_1mo_before_start_dict=data_1mo_before_start.to_dict()

        # key is the column name
        columns=list(data_1mo_before_start_dict.keys())
        # key2 is the timestamp
        key_time=list(data_1mo_before_start_dict[columns[0]].keys())
        start_date=pd.Timestamp(key_time[0])

        # the data for calculating financial indicators
        data=raw_data.loc[(raw_data.index >= start_date) & (raw_data.index <= pd_end)]

        # calculate simple moving average
        data['ma_short']=data['Close'].rolling(st.gdict['ma_short']).mean()
        data['ma_long']=data['Close'].rolling(st.gdict['ma_long']).mean()

        # calculate RSI
        daily_returns=data['Close'].diff()
        rsi_window=st.gdict['rsi_period']

        gain=daily_returns.clip(lower=0)
        loss=daily_returns.clip(upper=0)

        avg_gain=gain.rolling(rsi_window).mean()
        avg_loss=loss.rolling(rsi_window).mean()

        rsi=100-(100/(1+(avg_gain/abs(avg_loss))))

        data['rsi']=rsi

        # calculate the score of the stock based on the financial indicators
        ## buying:
        ### simple moving average
        buy_ma_signal=(data["ma_short"] > data["ma_long"]).astype(int)
        buy_ma_signal*=(st.gdict['ma_weight']/(st.gdict['ma_weight'] + st.gdict['rsi_weight']))

        ### RSI
        buy_rsi_signal=(data['rsi']<st.gdict['buy_rsi']).astype(int)
        buy_rsi_signal*=(st.gdict['rsi_weight']/(st.gdict['ma_weight'] + st.gdict['rsi_weight']))

        buy_signal=buy_ma_signal+buy_rsi_signal

        ## selling:
        ### simple moving average
        sell_ma_signal=(data["ma_short"] < data["ma_long"]).astype(int)
        sell_ma_signal*=(st.gdict['ma_weight']/(st.gdict['ma_weight'] + st.gdict['rsi_weight']))

        ### RSI
        sell_rsi_signal=(data['rsi']>st.gdict['sell_rsi']).astype(int)
        sell_rsi_signal*=(st.gdict['rsi_weight']/(st.gdict['ma_weight'] + st.gdict['rsi_weight']))

        sell_signal=sell_ma_signal+sell_rsi_signal

        # score for the stock
        data['signal_score']=buy_signal-sell_signal

        data['daily_returns']=data['Close'].pct_change()

        # leave the data for the period only
        data=data.loc[(data.index >= pd_start) & (data.index <= pd_end)]

        # return the data frame with scores of each stock
        return data

    # sorting the available stocks on a specified data
    # input:
    ## 1. date_timestamp: store date of the current round in the format of pandas timestamp
    ## 2. stocks_df[]: a list of the pandas dataframe of all available stocks
    ## 3. st: the strategy
    # output:
    ## 1. python dict{} storing the symbol and signal score in descenting order
    def sorting_stocks(self, date_timestamp, stocks_df, st):
        # store the selected stocks
        selected_stocks={}

        # iterate the stocks to select the stocks and their signal score
        for s in stocks_df:
            # select the current period
            stock=s.loc[(s.index == date_timestamp)]

            # checking the sell-off conditions
            stock_dict=stock.to_dict()

            ## current stock symbol
            symbol=(list(stock_dict.keys())[0][1])

            ## if the stock is in the portfolio
            if symbol in st.stocks.keys():
                ### checking 'stop loss'
                ### if the cumulative return was calculated for the stock in the portfolio, and the return is under the stop loss (stop loss should be negative, e.g. -3%)
                if st.stocks[symbol]['cumulative_return'] is not None and st.stocks[symbol]['cumulative_return'] < (-st.gdict['stop_loss']):
                    # this stock will not be selected
                    continue

                ### checking 'take profit'
                if st.stocks[symbol]['cumulative_return'] is not None and st.stocks[symbol]['cumulative_return'] > (st.gdict['take_profit']):
                    # this stock will not be selected
                    continue

            # getting the signal score
            selected_stocks[symbol]=stock_dict['signal_score', ''][date_timestamp]
        
        # sorting the selected stocks
        ## turn the scores of selected_stocks into numpy array
        signal_score_of_selected_stocks=np.array(list(selected_stocks.values()))
        selected_stock_symbol=np.array(list(selected_stocks.keys()))

        print('signal_score_of_selected_stocks= ', signal_score_of_selected_stocks)
        print('selected_stock_symbol= ', selected_stock_symbol)
        print('selected_stocks= ', selected_stocks)

        # print('ss= ',signal_score_of_selected_stocks)

        ## find the signal score of the stocks of top n signal score. n is the parameter generated from gene
        num_of_stock=st.gdict['num_of_stock']
        selected_score=signal_score_of_selected_stocks[np.argsort(a=signal_score_of_selected_stocks, kind='mergesort')[-num_of_stock:]]

        top_n_selected_stock_symbol=selected_stock_symbol[np.argsort(a=signal_score_of_selected_stocks, kind='mergesort')[-num_of_stock:]]

        print('selected_score= ', selected_score)
        print('top_n_selected_stock_symbol= ', top_n_selected_stock_symbol)

        return top_n_selected_stock_symbol
