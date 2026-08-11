import file_mgt
import validation
import os

# initialise hyper-parameters
run_id_file_path = 'CSV/run_id.csv'
## the number of run_id in the CSV file
### 0 means the first run_id, 1 means the second
num_of_run = 0

## the testing period
testing_fin_start = '2025-01-01'
testing_fin_end = '2025-12-31'

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

        # import training hyper-parameters
        hyper_parameter_file_name = 'JSON/' + str(run_id) + '/hyper_parameter.json'
    
        hyper_parameter = fm.read_json(filename=hyper_parameter_file_name)
        if hyper_parameter['run_id'] != run_id:
            print('<run_id> of hyper-parameter does not match!')
    
        # setting up hyper-parameters    
        trading_fee = hyper_parameter['trading_fee']
        start_up_cash = hyper_parameter['start_up_cash']
    
        num_of_generations = hyper_parameter['num_of_generations']
        num_of_elite = hyper_parameter['num_of_elite']
        pop_size = hyper_parameter['pop_size']
        point_mutate_rate = hyper_parameter['point_mutate_rate']
        point_mutate_amt = hyper_parameter['point_mutate_amt']

        # check file path availability of writing performance to JSON
        test_file_path = 'JSON/' + str(run_id) + '/testing_' + str(testing_fin_start) + '_' + str(testing_fin_end)
        if not fm.check_file_exist(test_file_path):
            os.mkdir(test_file_path)
    
        # run testing
        # validation
        valid = validation.Validation(
                val_fin_start = testing_fin_start,
                val_fin_end = testing_fin_end,
    
                # other parameters
                run_id = run_id,
                trading_fee = trading_fee,
                start_up_cash = start_up_cash,
    
                # file path:
                ## mainly for ga
                gene_spec_filename = hyper_parameter['gene_spec_filename'],
    
                ## sharing from ga to validation (for testing)
                elite_json_filepath = hyper_parameter['elite_json_filepath'],
                elite_csv_filepath = hyper_parameter['elite_csv_filepath'],
    
                ## for testing
                validation_hyper_parameter_filename = test_file_path + '/testing_hyper_parameter.json',
                is_testing=True
        )
    
        # run validation for the fittest strategy in each generation
        for gen in range(num_of_generations):
            for num_e in range(num_of_elite):
                # run validation for the input strategy
                valid.run_validation(
                    st_generation=gen, 
                    st_num=num_e, 
                    validation_performance_filename = test_file_path + '/testing_performance_gen' + str(gen) + '_elite' + str(num_e) + '.json'
                )
    else:
        print('<num_of_run> out of range. Please run training before this test.')  
else:
    print('<run_id> file not found')
    print('filepath: ', run_id_file_path)
