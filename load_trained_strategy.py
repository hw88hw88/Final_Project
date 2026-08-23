import file_mgt

class LoadTrainedStrategy:
    @staticmethod
    # get the run_id from CSV file
    # input:
    # 1. num_of_run: the number of run_id in the CSV file.
    ## For example, 0 means the first run_id in the CSV
    # output:
    # 1. run_id or None
    def get_run_id(num_of_run, run_id_file_path = 'CSV/run_id.csv'):
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
