import file_mgt
import strategy
import simulation
import pandas as pd

class Chatbot:
    # get the run_id from CSV file
    # input:
    # 1. num_of_run: the number of run_id in the CSV file.
    ## For example, 0 means the first run_id in the CSV
    # output:
    # 1. run_id or None
    @staticmethod
    def get_run_id(num_of_run = 0, run_id_file_path = 'CSV/run_id.csv'):
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
    # 1. run_id_file_path (optional): file path for <run_id>
    # 2. hyper_params_file_path (optional): file path for training hyper parameters
    # 3. gdict_file_path (optional): file path for gdict
    # output:
    # 1. trained strategy or None
    @staticmethod
    def get_strategy(
        run_id_file_path=None,
        hyper_params_file_path=None,
        gdict_file_path=None
        ):
        fm = file_mgt.FileMgt()
        # get run_id
        if run_id_file_path is None:
            run_id_file_path = 'CSV/run_id.csv'
        if fm.check_file_exist(run_id_file_path):
            with open (run_id_file_path) as f:
                csv_content = f.read()
            run_id = csv_content

            # get training hyper-parameters
            if hyper_params_file_path is None:
                hyper_params_file_path = 'JSON/' + str(run_id) + '/hyper_parameter.json'

            if fm.check_file_exist(hyper_params_file_path):
                hyper_params = fm.read_json(filename=hyper_params_file_path)
                num_of_gen = hyper_params.get('num_of_generations')

                # get gdict
                if gdict_file_path is None:
                    gdict_file_path = 'JSON/' + str(run_id) + '/fittest/elite_gdict_gen' + str(num_of_gen - 1) + '_0.csv'

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
                    return stgy
        return None

    # load data and financial indicators
    # input:
    # 1. trading_date: the date
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

