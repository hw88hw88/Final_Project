import api_fin_data
import pandas as pd
import numpy as np
from multiprocessing import Pool

class Simulation:
    # the setup of the simulation
    # input:
    # 1. fin_start: the date of the start of the period
    # 2. fin_end: the date of the end of the period
    # 3. trading_fee: the percentage of the trading fee. For example, 0.01 means 1% of the trading amount
    def __init__(self, fin_start, fin_end, trading_fee):
        self.api=api_fin_data.APIFinData()
        self.fin_start=fin_start
        self.fin_end=fin_end
        self.trading_fee=trading_fee

    # calculate the financial indicators for stock
    # input:
    # 1. st: strategy
    # 2. symbol: the stock code
    # output:
    # 1. pandas data frame storing the financial data and indicators of the stock
    def calculate_fin_indicator_for_stock(self, st, symbol, risk_free_interest_rate = 0.03):
        # retrieve the data from API or saved file
        raw_data=self.api.get_financial_data(symbol=symbol)
        if raw_data is None:
            return None

        # retrieve the data within the period
        pd_start=pd.Timestamp(self.fin_start)
        pd_end=pd.Timestamp(self.fin_end)

        # data 250 days before the start of the period for calculating financial indicators
        ## since the <ma_long> in gdict can be 250
        days_before_start = 250
        data_before_start=raw_data.loc[(raw_data.index <= pd_start)].tail(days_before_start)
        data_before_start_dict=data_before_start.to_dict()

        # key is the column name
        columns=list(data_before_start_dict.keys())
        # key2 is the timestamp
        key_time=list(data_before_start_dict[columns[0]].keys())
        if (len(key_time) < days_before_start):
            return None
        start_date=pd.Timestamp(key_time[0])

        # the data for calculating financial indicators for the selected period
        data=raw_data.loc[(raw_data.index >= start_date) & (raw_data.index <= pd_end)]
        if (len(key_time) < 1):
            return None

        # calculate simple moving average
        ## the shift of 1 row of closing price prevents look ahead bias
        data['ma_short']=data['Close'].shift(periods=1, axis=0).rolling(st.gdict['ma_short']).mean()
        data['ma_long']=data['Close'].shift(periods=1, axis=0).rolling(st.gdict['ma_long']).mean()

        # calculate RSI
        ## the shift of 1 row of closing price prevents look ahead bias
        ### the difference of amount (not percentage here)
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

        ## the shift of 1 row of closing price prevents look ahead bias
        data['daily_returns']=data['Close'].shift(periods=1, axis=0).pct_change()

        # calculating the Sharpe ratio for the stock

        # the number of trading days in a year is about 252 days
        ## Reference: https://www.stockgro.club/blogs/trading/how-many-trading-days-in-a-year/
        data['annualized_return'] = data['daily_returns'].mean() * 252
        data['annualized_volatility'] = data['daily_returns'].std() * np.sqrt(252)

        # calculating sharpe ratio
        data['sharpe_ratio'] = (data['annualized_return'] - risk_free_interest_rate) / data['annualized_volatility']

        # leave the data for the period only (removing the rows before the period, after calculating the financial indicators for the period)
        data=data.loc[(data.index >= pd_start) & (data.index <= pd_end)]

        # return the data frame with scores of each stock
        return data

    # sorting the available stocks on a specified data
    # input:
    # 1. date_timestamp: store date of the current round in the format of pandas timestamp
    # 2. stocks_df[]: a list of the pandas dataframe of all available stocks
    # 3. st: the strategy
    # output:
    # 1. numpy array storing the symbol of the selected stocks
    def sorting_stocks(self, date_timestamp, stocks_df, st):
        # store the selected stocks
        selected_stocks={}

        # iterate the stocks to select the stocks and their signal score
        for s in stocks_df:
            # select the current trading day (a day)
            stock=s.loc[(s.index == date_timestamp)]

            # convert to python dict{}
            stock_dict = stock.to_dict()

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
                # getting the sharpe ratio of the stock, and store the selected stock
                selected_stocks[symbol] = stock_dict['sharpe_ratio', ''][date_timestamp]

        # sorting the selected stocks, which is a dict{}, according to Sharpe ratio
        ## turn the scores of selected_stocks into numpy array
        sharpe_ratio_of_selected_stocks = np.array(list(selected_stocks.values()))
        ## turn the keys of selected_stocks into another numpy array
        selected_stock_symbol = np.array(list(selected_stocks.keys()))

        ## find the signal score of the stocks of top n signal score. 
        ## n which is the max_num_of_stock, is the parameter generated from gene.
        max_num_of_stock = st.gdict['max_num_of_stock']

        top_n_selected_stock_symbol = selected_stock_symbol[np.argsort(a=sharpe_ratio_of_selected_stocks)[-max_num_of_stock:]]

        # return a list
        return top_n_selected_stock_symbol.tolist()

    '''
    def run_creature(self, cr = None, cr_lifetime=2400):
            try:
                # initialize or reset the simulation
                pid = self.physicsClientId
                p.resetSimulation(physicsClientId=pid)
                p.setPhysicsEngineParameter(enableFileCaching=0, physicsClientId=pid)

                # load up sandbox and mountain
                mountain_env = cw_env.MountainEnv(pid)
                mountain_pos, arena_size = mountain_env.setup_environment()

                # I moved the setGtavity() here after setting up sandbox and mountain
                p.setGravity(0, 0, -10, physicsClientId=pid)

                # generate a random creature, if no input creature
                if cr == None:
                    cr = creature.Creature(gene_count=3)
                    print('New creature randomly generated because of missing input "cr"!')
                # convert the creature to XML and save it to URDF file
                xml_file = 'URDF/cr_' + str(self.sim_id) + '.urdf'
                xml_str = cr.to_xml()
                with open(xml_file, 'w') as f:
                    f.write(xml_str)

                # load the creature URDF file
                if self.is_handcrafted_urdf:
                    cid = p.loadURDF('URDF/handcraft/my_rob.urdf', basePosition = self.cr_start_pos, baseOrientation = self.cr_start_ori, physicsClientId=pid)
                else:
                    cid = p.loadURDF(xml_file, basePosition = self.cr_start_pos, baseOrientation = self.cr_start_ori, physicsClientId=pid)

                # airdrop the creature
                p.resetBasePositionAndOrientation(bodyUniqueId=cid, posObj=self.cr_start_pos, ornObj=self.cr_start_ori, physicsClientId=pid)

                # setup the environment (inform the creature the environment parameters)
                cr.setup_environment(m_pos=mountain_pos, arena_size=arena_size)

                # iterate the creature for its lifetime
                for frame in range(cr_lifetime):
                    # go to next step/ next frame of the simulation
                    p.stepSimulation(physicsClientId=pid)

                    # update the position of the creature
                    # ignore the first few seconds when the creature was being dropped from the air
                    if frame > 240 * 3:
                        pos, orn = p.getBasePositionAndOrientation(cid, physicsClientId=pid)
                        cr.update_position(pos)

                    # update the distance from the mountain to the creature
                    # if the distance is less than 0.1, stop the creature
                    # ignore the first few seconds when the creature was being dropped from the air
                    if frame > 240 * 3 + 1 and cr.get_distance_from_mountain() < 0.1:
                        self.motors.update_motors(cid=cid, cr=cr, p=p, pid=pid, isStop=True)
                    # update motors
                    elif frame % 24 == 0:
                        self.motors.update_motors(cid=cid, cr=cr, p=p, pid=pid)

            except Exception as e:
                print("sim failed cr links: ", len(cr.get_expanded_links()))
                print(e)

        # I added default value to input arguments
        def eval_population(self, pop, cr_lifetime):
            for cr in pop.creatures:
                self.run_creature(cr=cr, cr_lifetime=cr_lifetime)
    
    Title: CM3020 Artificial Intelligence, Week 10 Mid-term coursework
    Author: The author of this project (Anonoymous submission of assignment)
    Date: 2026
    Code version: N/A
    Availability: Submitted Assignment (Not published)
    (Week 10 Mid-term coursework of CM3020 Artificial Intelligence, 2026)

    The code in this function was adapted from the mid-term coursework in the week 10 of "CM3020 Artificial Intelligence" by the author of this project
    All the code was written and prepared by the author of this project.
    
    The code of the mid-term coursework was written with reference to the starter code from the mid-term coursework of "CM3020 Artificial Intelligence" (Yee-King, no date)

    Reference:
    Yee-King, M., (no date) CM3020 Artificial Intelligence, Week 10 Mid-term coursework starter code [online] Available from: https://www.coursera.org/learn/uol-cm3020-artificial-intelligence/assignment-submission/6JASg/mid-term-coursework [8 December 2025]

    '''

    # run the simulation of the investment
    # input:
    # 1. st: an investment strategy object
    # change:
    # 1. run the simulation of the investment
    # 2. call other methods to print the result on screen, and save the result to JSON and CSV files
    def run_strategy(self, st):
        # store the market data and the calculation of the financial indicators of each stock. The financial indicators were calculated based on the parameters in the strategy
        stocks_df=[]

        # get the symbol of available stocks in S&P500
        available_symbols=self.api.get_symbol_from_csv(fin_start=self.fin_start)

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


    '''
    def eval_population(self, pop, cr_lifetime):
        for cr in pop.creatures:
            self.run_creature(cr=cr, cr_lifetime=cr_lifetime)

    Title: CM3020 Artificial Intelligence, Week 10 Mid-term coursework
    Author: The author of this project (Anonoymous submission of assignment)
    Date: 2026
    Code version: N/A
    Availability: Submitted Assignment (Not published)
    (Week 10 Mid-term coursework of CM3020 Artificial Intelligence, 2026)

    The code in this function was adapted from the mid-term coursework in the week 10 of "CM3020 Artificial Intelligence" by the author of this project
    All the code was written and prepared by the author of this project.
    
    The code of the mid-term coursework was written with reference to the starter code from the mid-term coursework of "CM3020 Artificial Intelligence" (Yee-King, no date)

    Reference:
    Yee-King, M., (no date) CM3020 Artificial Intelligence, Week 10 Mid-term coursework starter code [online] Available from: https://www.coursera.org/learn/uol-cm3020-artificial-intelligence/assignment-submission/6JASg/mid-term-coursework [8 December 2025]
    '''
    # for the multi-threads version of simulation
    # input:
    # 1. pop: population instance
    def eval_population(self, pop):
        for st in pop.strategies:
            self.run_strategy(st=st)

    '''
    class ThreadedSim():
        def __init__(self, pool_size, cr_start_pos, cr_start_ori, is_handcrafted_urdf=False):
            self.sims = [Simulation(cr_start_pos=cr_start_pos, cr_start_ori=cr_start_ori, sim_id=i, is_handcrafted_urdf=is_handcrafted_urdf) for i in range(pool_size)]

    Title: CM3020 Artificial Intelligence, Week 10 Mid-term coursework
    Author: The author of this project (Anonoymous submission of assignment)
    Date: 2026
    Code version: N/A
    Availability: Submitted Assignment (Not published)
    (Week 10 Mid-term coursework of CM3020 Artificial Intelligence, 2026)

    The code in this function was adapted from the mid-term coursework in the week 10 of "CM3020 Artificial Intelligence" by the author of this project
    All the code was written and prepared by the author of this project.
    
    The code of the mid-term coursework was written with reference to the starter code from the mid-term coursework of "CM3020 Artificial Intelligence" (Yee-King, no date)

    Reference:
    Yee-King, M., (no date) CM3020 Artificial Intelligence, Week 10 Mid-term coursework starter code [online] Available from: https://www.coursera.org/learn/uol-cm3020-artificial-intelligence/assignment-submission/6JASg/mid-term-coursework [8 December 2025]
    '''

# Multi-threads version of simulation
# the class ThreadedSim implements the multi-threads operations of the simulation
# The code was adapted from the mid-term assignment of CM3020 Artificial Intelligence
# input (when creating the class): 
# 1. pool size:
# 2. trading_fee:
# 3. fin_start:
# 4. fin_end:
class ThreadedSim():
    def __init__(self, 
        trading_fee,
        pool_size, 
        fin_start=None,
        fin_end=None
    ):
        self.sims = [
            Simulation(
                trading_fee=trading_fee,
                fin_start=fin_start,
                fin_end=fin_end) for i in range(pool_size)
        ]

    '''
    @staticmethod
    def static_run_creature(sim, cr, cr_lifetime):
        sim.run_creature(cr=cr, cr_lifetime=cr_lifetime)
        return cr
    
    Title: CM3020 Artificial Intelligence, Week 10 Mid-term coursework
    Author: The author of this project (Anonoymous submission of assignment)
    Date: 2026
    Code version: N/A
    Availability: Submitted Assignment (Not published)
    (Week 10 Mid-term coursework of CM3020 Artificial Intelligence, 2026)

    The code in this function was adapted from the mid-term coursework in the week 10 of "CM3020 Artificial Intelligence" by the author of this project
    All the code was written and prepared by the author of this project.
    
    The code of the mid-term coursework was written with reference to the starter code from the mid-term coursework of "CM3020 Artificial Intelligence" (Yee-King, no date)

    Reference:
    Yee-King, M., (no date) CM3020 Artificial Intelligence, Week 10 Mid-term coursework starter code [online] Available from: https://www.coursera.org/learn/uol-cm3020-artificial-intelligence/assignment-submission/6JASg/mid-term-coursework [8 December 2025]
    '''

    @staticmethod
    def static_run_strategy(sim, st):
        sim.run_strategy(st=st)
        return st

    '''
    def eval_population(self, pop, cr_lifetime):
        """
        pop is a Population object
        cr_lifetime is frames in pybullet to run for at 240fps
        """
        pool_args = [] 
        start_ind = 0
        pool_size = len(self.sims)
        while start_ind < len(pop.creatures):
            this_pool_args = []
            for i in range(start_ind, start_ind + pool_size):
                if i == len(pop.creatures):# the end
                    break
                # work out the sim ind
                sim_ind = i % len(self.sims)
                this_pool_args.append([
                            self.sims[sim_ind], 
                            pop.creatures[i], 
                            cr_lifetime]   
                )
            pool_args.append(this_pool_args)
            start_ind = start_ind + pool_size

        new_creatures = []
        for pool_argset in pool_args:
            with Pool(pool_size) as po:
                # it works on a copy of the creatures, so receive them
                creatures = po.starmap(ThreadedSim.static_run_creature, pool_argset)
                # and now put those creatures back into the main 
                # self.creatures array
                new_creatures.extend(creatures)
        pop.creatures = new_creatures

    Title: CM3020 Artificial Intelligence, Week 10 Mid-term coursework
    Author: The author of this project (Anonoymous submission of assignment)
    Date: 2026
    Code version: N/A
    Availability: Submitted Assignment (Not published)
    (Week 10 Mid-term coursework of CM3020 Artificial Intelligence, 2026)

    The code in this function was adapted from the mid-term coursework in the week 10 of "CM3020 Artificial Intelligence" by the author of this project
    All the code was written and prepared by the author of this project.
    
    The code of the mid-term coursework was written with reference to the starter code from the mid-term coursework of "CM3020 Artificial Intelligence" (Yee-King, no date)

    Reference:
    Yee-King, M., (no date) CM3020 Artificial Intelligence, Week 10 Mid-term coursework starter code [online] Available from: https://www.coursera.org/learn/uol-cm3020-artificial-intelligence/assignment-submission/6JASg/mid-term-coursework [8 December 2025]
    '''

    def eval_population(self, pop):
        pool_args = [] 
        start_ind = 0
        pool_size = len(self.sims)
        while start_ind < len(pop.strategies):
            this_pool_args = []
            for i in range(start_ind, start_ind + pool_size):
                if i == len(pop.strategies):# the end
                    break
                # work out the sim ind
                sim_ind = i % len(self.sims)
                this_pool_args.append([
                            self.sims[sim_ind], 
                            pop.strategies[i]]                            
                )
            pool_args.append(this_pool_args)
            start_ind = start_ind + pool_size

        new_strategies = []
        for pool_argset in pool_args:
            with Pool(pool_size) as po:
                # it works on a copy of the strategies, so receive them
                strategies = po.starmap(ThreadedSim.static_run_strategy, pool_argset)
                # and now put those strategies back into the main self.strategies array
                new_strategies.extend(strategies)
        pop.strategies = new_strategies