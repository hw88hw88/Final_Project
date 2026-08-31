import file_mgt
import strategy
import simulation
import pandas as pd
import datetime
import re
import json

from llama_cpp import Llama

class Chatbot:
    # initialize the chatbot
    # the function runs after being called, not run automatically at the start
    def initialize_chatbot(
        self,
        model_path = "LLM/gemma-4-E2B-it-qat-q4_0-gguf/gemma-4-E2B_q4_0-it.gguf"
        ):
        ## loading the LLM
        self.llm = Llama(
            model_path=model_path, 
            n_gpu_layers=-1,
            n_ctx=4096,
        )
    # get the run_id from CSV file
    # input:
    # 1. num_of_run: the number of run_id in the CSV file.
    # 2. run_id_file_path: the file path of CSV file storing the run_id
    ## For example, 0 means the first run_id in the CSV
    # output:
    # 1. run_id
    # 2. None, if run_id cannot be retrieved
    @staticmethod
    def get_run_id(
        num_of_run = 0, 
        run_id_file_path = 'CSV/run_id.csv',
        ):
        fm = file_mgt.FileMgt()

        # import <run_id> from a list
        if fm.check_file_exist(run_id_file_path):
            with open (run_id_file_path) as f:
                csv_content = f.read()
                # separate each element
                csv_content = csv_content.split(',')

            # remove space ' ' from <csv_content>
            i = len(csv_content) - 1
            while i >= 0:
                csv_content[i] = csv_content[i].strip()
                if len(csv_content[i]) < 1:
                    csv_content.pop(i)
                i -= 1

            # determine the <run_id> from the list from file
            if len(csv_content) > 0:
                if num_of_run < len(csv_content):
                    run_id = csv_content[num_of_run]
                else:
                    print('<num_of_run> out of range. It has been set to 0.')
                    run_id = csv_content[0]
                return run_id
            else:
                print('There is no <run_id>. Please run the training first.')
        return None

    # read the trained strategy amd return
    # input:
    # 1. run_id: <run_id>
    # 2. hyper_params_file_path (optional): file path for training hyper parameters
    # 3. gdict_file_path (optional): file path for gdict
    # output:
    # 1. trained strategy: investment strategy
    # 2. gdict: the gene dictionary of strategy
    # 3. None, if either hyper-parameters of the training or gdict cannot be retrieved
    @staticmethod
    def get_strategy(
        run_id,
        hyper_params_file_path=None,
        gdict_file_path=None
        ):
        fm = file_mgt.FileMgt()
        # get training hyper-parameters
        ## (the file path depends on the run_id, so it is assigned here, rather than the input parameters)
        if hyper_params_file_path is None:
            hyper_params_file_path = 'JSON/' + str(run_id) + '/hyper_parameter.json'

        if fm.check_file_exist(hyper_params_file_path):
            hyper_params = fm.read_json(filename=hyper_params_file_path)
            num_of_gen = hyper_params.get('num_of_generations')

            # get gdict
            ## (the file path depends on the run_id, so it is assigned here, rather than the input parameters)
            if gdict_file_path is None:
                gdict_file_path = 'JSON/' + str(run_id) + '/fittest/elite_gdict_gen' + str(num_of_gen - 1) + '_0.json'

            if fm.check_file_exist(gdict_file_path):
                gdict = fm.read_json(
                    filename=gdict_file_path
                )

                # get gene for storing the gene in strategy instance
                gene_file_path = 'CSV/' + str(run_id) + '/fittest/elite_gene_gen' + str(num_of_gen - 1) + '_0.csv'

                gene = None

                if fm.check_file_exist(gene_file_path):
                    gene = fm.read_from_csv(
                        csv_file_path=gene_file_path
                    )

                stgy = strategy.Strategy(
                    start_up_cash=100000, 
                    gdict=gdict,
                    gene=gene
                    )
                return stgy, gdict
        return None, None

    # load data and financial indicators
    # input:
    # 1. trading_date: the trading date
    # 2. st: investment strategy instance
    # 3. trading_fee: e.g. 0.01 means 1% of the trading amount
    # output:
    # 1. a list of data frame of all stocks
    @staticmethod
    def get_data(
            trading_date,
            st,
            trading_fee=0.01):

        # setting the start and end the same date to get the financial data on the trading day
        sim = simulation.Simulation(
            fin_start = trading_date,
            fin_end = trading_date,
            trading_fee = trading_fee
            )

        # getting the data frame of all stocks
        stocks_df = sim.get_stock_fin_indicator(
            st = st
            )
        return stocks_df

    # generating the target portfolio
    # input:
    # 1. st: investment strategy
    # 2. stocks_df: the data frame of all available stocks of S&P500
    # 3. trading_date: (str) the trading date in the format 'yyyy-mm-dd'
    # 4. trading_fee: the trading fee. E.g. 0.01 means 1% of the transaction amount
    # output:
    # 1. current_target_portfolio: a list of symbols of the target stocks
    @staticmethod
    def get_investment_portfolio(
            st,
            stocks_df,
            trading_date,
            trading_fee=0.01
        ):
        # setting the start and end the same date to get the financial data on the trading day
        sim = simulation.Simulation(
            fin_start = trading_date,
            fin_end = trading_date,
            trading_fee = trading_fee
            )

        current_target_portfolio = sim.sorting_stocks(
            date_timestamp=pd.Timestamp(trading_date), 
            stocks_df=stocks_df.copy(), 
            st=st)

        return current_target_portfolio

    # retrieving the financial information and the calculated financial indicators of the target portfolio for the chatbot
    # input:
    # 1. trading_date: (str) the trading date in the format 'yyyy-mm-dd'
    # 2. num_of_run: (int) the run id number. E.g. 0 means the first run_id in the CSV file
    # 3. trading_fee: (float) the trading fee. E.g. 0.01 means 1% of the trading amount
    # output:
    # 1. portfolio: a list of stock symbols
    # 2. portfolio_dict: a dictionary of information of stocks in portfolio
    # 3. st: an investment strategy
    # 4. gdict: dictionary of gene of strategy
    def apply_strategy(
        self,
        trading_date,
        num_of_run = 0,
        trading_fee = 0.01,
        run_id_file_path = 'CSV/run_id.csv',
        hyper_params_file_path=None,
        gdict_file_path=None
        ):
        run_id = self.get_run_id(
            num_of_run = num_of_run,
            run_id_file_path = run_id_file_path,
            )

        st, gdict = self.get_strategy(
            run_id = run_id,
            hyper_params_file_path=hyper_params_file_path,
            gdict_file_path=gdict_file_path,
        )

        if st is None:
            print('st is None')
            return None

        stocks_df = self.get_data(
            trading_date = trading_date,
            st = st,
            trading_fee = trading_fee)

        portfolio = self.get_investment_portfolio(
            st = st,
            stocks_df = stocks_df,
            trading_date = trading_date,
            trading_fee=trading_fee
        )

        # store the portfolio stock data
        portfolio_dict = {}

        for stock_df in stocks_df:
            # convert to python dict{}
            stock_dict = stock_df.to_dict()

            ## current stock symbol
            symbol=(list(stock_dict.keys())[0][1])

            if symbol in portfolio:
                portfolio_dict[symbol] = {
                    'symbol': symbol,
                    'price': list(stock_dict['Close', str(symbol)].values())[0],
                    'ma_short': list(stock_dict['ma_short', ''].values())[0],
                    'ma_long': list(stock_dict['ma_long', ''].values())[0],
                    'rsi': list(stock_dict['rsi', ''].values())[0],
                    # 'signal_score': list(stock_dict['signal_score', ''].values())[0],
                    'daily_return': list(stock_dict['daily_returns', ''].values())[0],
                    'annualized_return': list(stock_dict['annualized_return', ''].values())[0],
                    'sharpe_ratio': list(stock_dict['sharpe_ratio', ''].values())[0],
                    'annualized_volatility': list(stock_dict['annualized_volatility', ''].values())[0],
                }

        return portfolio, portfolio_dict, st, gdict

    # generate the chatbot response
    # input:
    # 1. portfolio
    # 2. portfolio_dict
    # 3. trading_date
    # output:
    # 1. output: the text output of the LLM
    def generate_advice(self, portfolio, portfolio_dict, trading_date):
        # initialize the chatbot at the first time of running
        if getattr(self, 'llm', None) is None:
            self.initialize_chatbot()

        # prepare the prompt
        prompt = f"""
        You are a professional financial advisor. I am a system analyzing the S&P 500 stocks to generate an investment portfolio containing the stock(s) {portfolio} to the user.
        """

        for p in portfolio:
            prompt = prompt + f"""
                stock: {portfolio_dict.get(p).get('symbol')}
                Price on {trading_date}: {portfolio_dict.get(p).get('price')}
                Financial indicators:
                Short SMA = {portfolio_dict.get(p).get('ma_short')}
                Long SMA = {portfolio_dict.get(p).get('ma_long')}
                RSI = {portfolio_dict.get(p).get('rsi')}
                Sharpe ratio = {portfolio_dict.get(p).get('sharpe_ratio')}
            """

        prompt = prompt + """
            Please provide investment recommendations to the user. Explain the recommendations based on the financial indicators provided. Please reply to the user on behalf of me directly and do not quote me.
            """

        try:
            output = self.llm(
                'User: ' + prompt + '. Assistant: ',
                max_tokens=10240,
                stop=["User:"],
                echo=False
            )
            raw_response = output.get('choices', [])
            if not raw_response:
                raise ValueError
            return raw_response[0].get('text', '')
        except Exception as e:
            print('Error: ', e)
            return ''

    # classify the user input with the LLM
    # input:
    # 1. user_prompt: (str) user prompt
    # output:
    # 1. a dict of result
    def identify_user_input(self, user_prompt):
        # initialize the chatbot at the first time of running
        if getattr(self, 'llm', None) is None:
            self.initialize_chatbot()

        # prepare the prompt
        today_date = datetime.datetime.now()
        today_date = today_date.strftime('%Y-%m-%d')

        prompt = f"""Today's date is {today_date}.

        You are a professional financial advisor. Your task is to classify user input into a JSON object.

        Rules:
        1. greeting: boolean (true if the user says hello, hi, etc.)
        2. investment: boolean (true if the user expresses intent to invest)
        3. investment_explanation: boolean (true if the user ask for explanation of recommendations)
        4. prefer_low_risk: boolean (true if the user mentions safety, or conservative goals)
        5. investment_date: string ('yyyy-mm-dd' or null).
        - If no date is mentioned: null.
        - If a future date is mentioned: {today_date}.
        - If a past date is mentioned: that specific date.

        Example Output Format:
        {{"greeting": false, "investment": true, "investment_explanation": false, "prefer_low_risk": false, "investment_date": null}}

        User Input: "{user_prompt}"

        Return ONLY the JSON object."""

        try:
            output = self.llm(
                'User: ' + prompt + '. Assistant: ',
                max_tokens=200,
                stop=["User:"],
                echo=False,
                temperature=0,
            )

            raw_response = output.get('choices', [])
            if not raw_response:
                raise ValueError
            raw_response = raw_response[0].get('text', '')
            response = re.search(r'\{.*\}', raw_response, re.S)
            if response:
                return json.loads(response.group())
            return {"greeting": False, "investment": False, "investment_explanation": False, "prefer_low_risk": False, "investment_date": None, "error": "Invalid response", "raw_response": raw_response}
        except Exception as e:
            print('Error: ', e)
            return {"greeting": False, "investment": False, "investment_explanation": False, "prefer_low_risk": False, "investment_date": None, "error": str(e), "raw_response": raw_response}

    def generate_custom_response(self, stock, fin_indicators):
        pass