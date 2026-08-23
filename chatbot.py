import file_mgt
import strategy

class Chatbot:
    # read the trained strategy amd return
    # input:
    # 1. run_id_file_path (optional): file path for <run_id>
    # 2. hyper_params_file_path (optional): file path for training hyper parameters
    # 3. gdict_file_path (optional): file path for gdict
    # output:
    # 1. trained strategy or None
    @staticmethod
    def get_strategy(run_id_file_path=None,
                     hyper_params_file_path=None,
                     gdict_file_path=None):
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

