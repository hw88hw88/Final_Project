import genome
import numpy as np

class Strategy:
    def __init__(self, start_up_cash):
        # record the performance
        self.rewards=0
        self.cumulative_return=0
        self.stocks={}
        self.stock_cumulative_return={}
        # self.annual_return=0
        self.max_drawdown=0
        # self.sharpe_ratio=None
        self.num_of_increase_in_value=0
        self.age=0
        self.num_of_trade=0
        self.cash=start_up_cash
        self.start_up_cash=start_up_cash

        # the value of the portfolio
        self.total_value=self.cash
        self.high_value=self.cash
        self.low_value=self.cash
        self.total_value_sequence=[]

        # the configuration or structure of the strategy
        spec=genome.Genome.get_gene_spec()
        gene=genome.Genome.get_random_gene(len(spec))
        self.gdict=genome.Genome.get_gdict(
            gene=gene,
            spec=spec
        )

    # retrieve the market price and volume from the input data
    # input:
    # 1. current_trading_date: pandas timestamp of the date of the trading date
    # 2. stock_df: pandas data frame of a stock
    # 3. symbol: the symbol of the stock, such as 'MSFT' or 'AAPL'
    # output:
    # 1. current price of the share
    # 2. the market volume on the current trading day
    def get_market_info(self, current_trading_date, stock_df, symbol):
        ## get the current information of the stock on the market
        ### get the data on the current date
        current_this_stock = stock_df.loc[stock_df.index == current_trading_date]
        ### convert to dict{}
        current_this_stock_dict = current_this_stock.to_dict()

        ## finding the price & volume of the stock
        current_price=current_this_stock_dict['Close', symbol][current_trading_date]
        market_volume=current_this_stock_dict['Volume', symbol][current_trading_date]

        return {'current_price': current_price, 'market_volume': market_volume}

    # a function to add a stock to the portfolio
    # input:
    # 1. current_trading_date: pandas timestamp of the date of the trading date
    # 2. stock_df: pandas data frame of a stock to be bought
    # 3. current_target_portfolio: a list of symbols of target stocks of a new portfolio
    # 4. symbol: the symbol of the stock to be bought, such as 'MSFT' or 'AAPL'
    # 5. trading_fee: the fee for trading the stocks in percentage of the stock price
    # change: (the change it makes, not the return value)
    # 1. deduct self.cash to buy shares
    # 2. add to self.stocks{} the volume, date, cost of the newly bought shares
    # 3. add self.num_of_trade by 1
    # 4. add the symbol to self.stock_cumulative_return[symbol]
    def buy_stock(self, 
                  current_trading_date, 
                  stock_df, 
                  current_target_portfolio, 
                  symbol,
                  trading_fee):
        # get market information
        mkt_info=self.get_market_info(current_trading_date=current_trading_date,
                                      stock_df=stock_df,
                                      symbol=symbol)
        current_price = mkt_info['current_price']
        market_volume = mkt_info['market_volume']

        ## the value and volume to be bought
        target_num_of_stocks = len(current_target_portfolio)

        target_value = int(np.floor(self.cash / target_num_of_stocks))
        target_volume = int(np.floor(target_value / (current_price + trading_fee)))

        ### check if the volume is larger than market volume (very rarely)
        target_volume = min(target_volume, market_volume)

        ## reduce cash
        buying_cost = target_volume * (current_price + trading_fee)
        self.cash -= buying_cost

        ## get the shares
        self.stocks[symbol]={
            'volume': target_volume, 
            'date': current_trading_date, 
            'cost': buying_cost,
            }

        ## add number of trade
        self.num_of_trade+=1
        ## add the cumulative return for each stock
        self.stock_cumulative_return[symbol]=0

    # a function to remove a stock from the portfolio
    # input:
    # 1. current_trading_date: pandas timestamp of the date of the trading date
    # 2. stock_df: pandas data frame of a stock to be sold
    # 3. symbol: the symbol of the stock to be sold, such as 'MSFT' or 'AAPL'
    # 4. trading_fee: the fee for trading the stocks in percentage of the stock price
    # change:
    # 1. add the cash (receiving money by selling the stock)
    # 2. remove the stock from portfolio
    # 3. add number of trades
    def sell_stock(self,
                  current_trading_date,
                  stock_df,
                  symbol,
                  trading_fee):

        # get market information
        mkt_info=self.get_market_info(current_trading_date=current_trading_date,
                                      stock_df=stock_df,
                                      symbol=symbol)
        current_price = mkt_info['current_price']
        market_volume = mkt_info['market_volume']

        # calculate the volume of the shares to be sold
        volume_to_sell = self.stocks[symbol]['volume']
        ### check if the volume is larger than market volume (very rarely)
        volume_to_sell = min(market_volume, volume_to_sell)

        # receiving cash
        self.cash += volume_to_sell * (current_price - trading_fee)

        # deducting the stock from the portfolio
        self.stocks.pop(symbol)
        self.stock_cumulative_return.pop(symbol)

        self.num_of_trade+=1

    # update the value of the stock and portfolio
    # input:
    # 1. stocks_df[]: a list of the pandas dataframe of all available stocks
    # 2. current_trading_date: pandas timestamp of the date of the trading date
    # 3. trading_fee: the fee for trading the stocks in percentage of the stock price
    # changes:
    # 1. update self.stock_cumulative_return[symbol], if the stock is in the portfolio
    # 2. update self.high_value, which stores the highest value of the total value of the portfolio
    # 3. update self.low_value, which stores the lowest value of the total value of the portfolio
    # 4. update self.cumulative_return, which is the cumulative return of the portfolio
    # 5. update self.total_value, which is the total value of the portfolio
    # 6. update self.num_of_increase_in_value, which is the number of times the value of the portfolio increase
    # 7. update self.max_drawdown, which is the highest
    def daily_update(self, 
                     stocks_df,
                     current_trading_date,
                     trading_fee
                     ):
        # initialise the new total value of portfolio
        new_portfolio_value = 0

        # iterate the stocks on the market
        for s in stocks_df.copy():
            # select the current trading date
            stock_df=s.loc[(s.index == current_trading_date)]

            # convert to python dict{}
            stock_dict=stock_df.to_dict()

            ## find the current stock symbol
            symbol=(list(stock_dict.keys())[0][1])

            ## if the stock is in the portfolio
            if symbol in list(self.stocks.keys()):
                # volume and cost of the stock in portfolio
                cost = self.stocks[symbol]['cost']
                volume = self.stocks[symbol]['volume']

                # get market information
                mkt_info=self.get_market_info(
                                            current_trading_date=current_trading_date,
                                            stock_df=stock_df,
                                            symbol=symbol
                                            )

                current_price = mkt_info['current_price']

                # check the stop-loss strategy
                if current_price < cost / volume * (1 + self.gdict['stop_loss']):
                    # sell the stock
                    self.sell_stock(
                                current_trading_date=current_trading_date,
                                stock_df=stock_df,
                                symbol=symbol,
                                trading_fee=trading_fee)
                    # the stock was sold and removed from portfolio
                    continue

                # check the take-profit strategy
                if current_price > cost / volume * (1 + self.gdict['take_profit']):
                    # sell the stock
                    self.sell_stock(
                                current_trading_date=current_trading_date,
                                stock_df=stock_df,
                                symbol=symbol,
                                trading_fee=self.trading_fee)
                    # the stock was sold and removed from portfolio
                    continue

                # update the stock_cumulative_return
                self.stock_cumulative_return[symbol] = volume * current_price - cost

                # adding to portfolio value
                new_portfolio_value += volume * current_price

        # calculate the portfolio value, by adding the value of all stocks and cash in the portfolio
        new_portfolio_value += self.cash

        # update the portfolio value, high, low
        if new_portfolio_value >= self.total_value:
            self.num_of_increase_in_value += 1

        self.high_value = max(new_portfolio_value, self.high_value)
        self.low_value = min(new_portfolio_value, self.low_value)

        self.total_value = new_portfolio_value
        self.total_value_sequence.append(self.total_value)

        # update maximum drawdown of the portfolio
        portfolio_value_peak = np.maximum.accumulate(self.total_value_sequence)
        drawdown = (self.total_value - portfolio_value_peak) / portfolio_value_peak
        self.max_drawdown = max(drawdown)

        self.cumulative_return = self.total_value - self.start_up_cash

        # update the age of the portfolio
        self.age += 1

    # this function perform the rebalancing of portfolio. The rebalancing will reset the portfolio to the target stocks
    # input:
    # 1. current_target_portfolio[]: numpy array storing the symbol of the target selected stocks
    # 2. stocks_df[]: the market data and the calculation of the financial indicators of each stock. The financial indicators were calculated based on the parameters in the strategy
    # 3. current_trading_date: the current trading date in the format of pandas timestamp
    # 4. trading_fee: 
    # change:
    # 1. the stocks of the portfolio will become the target stocks
    def rebalance(self, 
                  current_target_portfolio, 
                  stocks_df, 
                  current_trading_date,
                  trading_fee):
        ## if no stock in the portfolio
        if len(list(self.stocks.keys())) == 0:
            for symbol in current_target_portfolio:
                for stock_df in stocks_df:
                    ## find the stock from data
                    stock_dict=stock_df.to_dict()
                    s_df_symbol=(list(stock_dict.keys())[0][1])

                    # if the stock was found
                    if s_df_symbol == symbol:
                        # buy the stocks
                        self.buy_stock(
                            current_trading_date=current_trading_date, 
                            stock_df=stock_df, 
                            current_target_portfolio=current_target_portfolio, 
                            symbol=symbol,
                            trading_fee=trading_fee,
                            )
                        break
        else:
            # there are stocks in the portfolio
            ## matching the current portfolio with target portfolio
            symbols_in_portfolio=list(self.stocks.keys())
            matched_stock_in_portfolio_index=[]
            for s_in_portfolio in symbols_in_portfolio:
                for s_target_portfolio in current_target_portfolio:
                    if s_in_portfolio == s_target_portfolio:
                        matched_stock_in_portfolio_index.append(s_in_portfolio)
                        break

            ## selling the unmatched stocks in the portfolio
            for s_in_p in symbols_in_portfolio:
                if s_in_p not in matched_stock_in_portfolio_index:
                    ### for all stocks in portfolio not in the matched list, which is a list of stocks to be held
                    for stock_df in stocks_df:
                        ### find the stock from data, then sell it
                        stock_dict=stock_df.to_dict()
                        s_df_symbol=(list(stock_dict.keys())[0][1])

                        #### if the stock was found, sell it
                        if s_df_symbol == s_in_p:
                            self.sell_stock(
                                current_trading_date=current_trading_date,
                                stock_df=stock_df,
                                symbol=s_in_p,
                                trading_fee=trading_fee,
                                )

            ## adding the target stocks to the portfolio if the stock not in the portfolio
            for target_stock in current_target_portfolio:
                if target_stock not in symbols_in_portfolio:
                    ### find the stock data
                    for stock_df in stocks_df:
                        ### find the stock from data, then buy it
                        stock_dict=stock_df.to_dict()
                        s_df_symbol=(list(stock_dict.keys())[0][1])

                        if s_df_symbol == target_stock:
                            self.buy_stock(
                                current_trading_date=current_trading_date, 
                                stock_df=stock_df, 
                                current_target_portfolio=current_target_portfolio, 
                                symbol=s_df_symbol,
                                trading_fee=trading_fee,
                            )

    def fitness(self):
        pass
