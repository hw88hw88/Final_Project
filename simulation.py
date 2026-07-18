import api_fin_data
import pandas as pd
import numpy as np

class Simulation:
    def __init__(self, fin_start, fin_end, trading_fee):
        self.api=api_fin_data.APIFinData()
        self.fin_start=fin_start
        self.fin_end=fin_end
        self.trading_fee=trading_fee

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
        if (len(key_time) <40):
            print('Error: Not enough data for symbol= ', symbol)
            return None
        start_date=pd.Timestamp(key_time[0])

        # the data for calculating financial indicators
        data=raw_data.loc[(raw_data.index >= start_date) & (raw_data.index <= pd_end)]
        if (len(key_time) < 1):
            print('Error: Not enough data for symbol= ', symbol)
            return None

        # calculate simple moving average
        ## the shift of 1 row of closing price prevents look ahead bias
        data['ma_short']=data['Close'].shift(periods=1, axis=0).rolling(st.gdict['ma_short']).mean()
        data['ma_long']=data['Close'].shift(periods=1, axis=0).rolling(st.gdict['ma_long']).mean()

        # calculate RSI
        ## the shift of 1 row of closing price prevents look ahead bias
        daily_returns=data['Close'].shift(periods=1, axis=0).diff()
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

        # leave the data for the period only (removing the rows before the period, after calculating the financial indicators for the period)
        data=data.loc[(data.index >= pd_start) & (data.index <= pd_end)]

        # return the data frame with scores of each stock
        return data

    # sorting the available stocks on a specified data
    # input:
    ## 1. date_timestamp: store date of the current round in the format of pandas timestamp
    ## 2. stocks_df[]: a list of the pandas dataframe of all available stocks
    ## 3. st: the strategy
    # output:
    ## 1. numpy array storing the symbol of the selected stocks
    def sorting_stocks(self, date_timestamp, stocks_df, st):
        # store the selected stocks
        selected_stocks={}

        # iterate the stocks to select the stocks and their signal score
        for s in stocks_df:
            # select the current period
            stock=s.loc[(s.index == date_timestamp)]

            # convert to python dict{}
            stock_dict=stock.to_dict()

            ## current stock symbol
            symbol=(list(stock_dict.keys())[0][1])

            ## if the stock is in the portfolio
            if symbol in st.stocks.keys():
                if st.stock_cumulative_return[symbol] is not None:
                    stock_cumulative_return = st.stock_cumulative_return[symbol]
                    ### checking 'stop loss'
                    ### if the cumulative return was calculated for the stock in the portfolio, and the return is under the stop loss (stop loss should be negative, e.g. -3%)
                    if stock_cumulative_return < (-1 * abs(st.gdict['stop_loss'])):
                        # this stock will not be selected
                        continue

                    ### checking 'take profit'
                    if stock_cumulative_return > (st.gdict['take_profit']):
                        # this stock will not be selected
                        continue

            # checking the signal score
            ## give up the stocks if the signal score is negative
            if stock_dict['signal_score', ''][date_timestamp] <= 0:
                continue
            else:
                # getting the signal score, and store the selected stock
                selected_stocks[symbol]=stock_dict['signal_score', ''][date_timestamp]

        # sorting the selected stocks
        ## turn the scores of selected_stocks into numpy array
        signal_score_of_selected_stocks=np.array(list(selected_stocks.values()))
        selected_stock_symbol=np.array(list(selected_stocks.keys()))

        ## find the signal score of the stocks of top n signal score. n is the parameter generated from gene
        max_num_of_stock=st.gdict['max_num_of_stock']

        top_n_selected_stock_symbol=selected_stock_symbol[np.argsort(a=signal_score_of_selected_stocks, kind='mergesort')[-max_num_of_stock:]]

        return top_n_selected_stock_symbol.tolist()

    # calculating the performance of the input strategy
    # input:
    ## 1. st: an investment strategy
    # change:
    ## 1. 
    def run_strategy(self, st):
        # store the market data and the calculation of the financial indicators of each stock. The financial indicators were calculated based on the parameters in the strategy
        stocks_df=[]

        # get the symbol of available stocks in S&P500
        available_symbols=self.api.get_symbol_from_csv()

        # calculating the financial indicators of each stock with the parameters in the strategy
        ## get the financial data and indicators
        for symbol in available_symbols:
            result=self.calculate_fin_indicator_for_stock(st=st, symbol=symbol)
            # the result is None, when the data of the stock is empty or not enough in the period (from self.fin_start to self.fin_end). Then, the stock will be not be selected in the period.
            if result is not None:
                stocks_df.append(result)

        # initialise trading day counter
        count_trading_day=0

        # initialise current trading date
        current_trading_date=None

        # the last trading date
        last_trading_date=pd.Timestamp(self.api.get_nth_date(stocks_df[0], n=-1))

        # iterate the trading day, until reaching the last trading date
        while (current_trading_date is None) or (current_trading_date != last_trading_date):
            
            # the current date of the simulation might not be a trading day. It might be a holiday.
            # finding the nearest trading day on or after the current date
            ## the first trading date in the financial data
            current_trading_date=pd.Timestamp(self.api.get_nth_date(stocks_df[0], n=count_trading_day))
            
            print('count_trading_day= ', count_trading_day, ' current_trading_date= ', current_trading_date)

            # rebalancing every st.gdict['num_of_day_rebalance'] trading day (include the first day).
            ## rebalancing means resetting the portfolio to the target
            ## the target is the portfolio having the top n highest signal score of stocks
            if count_trading_day % st.gdict['num_of_day_rebalance'] ==0:
                # selecting the target stocks for the portfolio on the current trading date of the simulation
                current_target_portfolio=self.sorting_stocks(date_timestamp=current_trading_date, stocks_df=stocks_df.copy(), st=st)

                # rebalance the portfolio
                st.rebalance(
                    current_target_portfolio=current_target_portfolio, 
                    stocks_df=stocks_df.copy(), 
                    current_trading_date=current_trading_date,
                    trading_fee=self.trading_fee,
                    )

            # sell all stocks on the last day to get the total value after deducting trading fee
            if current_trading_date == last_trading_date:
                for stock_in_portfolio in list(st.stocks.keys()):
                    for stock_on_market in stocks_df:
                        ## find the stock from data
                        stock_dict=stock_on_market.to_dict()
                        s_df_symbol=(list(stock_dict.keys())[0][1])

                        # sell all stocks in portfolio
                        if s_df_symbol == stock_in_portfolio:
                            st.sell_stock(
                                current_trading_date=current_trading_date,
                                stock_df=stock_on_market,
                                symbol=s_df_symbol,
                                trading_fee=self.trading_fee)

            # update strategies
            st.daily_update(stocks_df=stocks_df.copy(),
                            current_trading_date=current_trading_date,
                            trading_fee=self.trading_fee
                            )

            # go to next trading day
            count_trading_day += 1
