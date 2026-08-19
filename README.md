# Final_Project
My final project for academic review only.

## Notice
This repository is for academic review only.

All rights reserved. No permission is granted to use, copy, modify, or distribute this code without explicit permission from the author.

### The file structure of the GA

ga/
│    # stores all CSV files
├── CSV/
│   │    # a csv file storing the symbols of all S&P500 stocks
│   ├── S&P 500 Historical Components & Changes (Updated).csv
│   │    # storing all S&P500 stock symbols downloaded from yfinance
│   ├── downloadable_stock_code.csv
│   │    # storing all S&P500 stock symbols that 
│   │    # could not be downloaded from yfinance
│   ├── undownloadable_stock_code.csv
│   │    # a folder storing all financial data in csv format
│   ├── stock_data
│   │   │    # each csv stores the financial data of a stock
│   │   │    ## e.g. "AAPL_max.csv"
│   │   └── <symbol>_max.csv
│   │    # a folder storing all csv files with the same run_id
│   ├── <run_id>
│   │   │    # a folder storing genes of investment strategies
│   │   └── fittest
│   │       │    # the genes of the fittest in a generation
│   │       │    ## e.g. "elite_gene_gen0_1.csv"
│   │       │    ## the second fittest strategy in the first generation
│   │       └── elite_gene_gen<number of generation>_<elite number>.csv
│   │    # a csv file storing all run_id
│   └── run_id.csv
│    # stores all JSON files
├── JSON/
│   │    # a folder storing all JSON files with the same run_id
│   └── <run_id>
│       │    # the result of the performance in the training and validation
│       ├── ga_performance.json
│       │    # the gene specification in JSON format
│       ├── gene_spec.json
│       │    # the hyper-parameters for the training
│       ├── hyper_parameter.json
│       │    # the hyper-parameters for the validation
│       ├── validation_hyper_parameter.json
│       │    # a folder to store the gdict of 
│       │    # the fittest in the training process
│       ├── fittest
│       │    │     # the JSON files of gdict
│       │    │     ## e.g. "elite_gdict_gen0_0.json"
│       │    └── elite_gdict_gen<generation number>_<elite number>.json
│       │    # a folder storing the hyper-parameters and 
│       │    # performance of the strategies in the testing process
│       │    # e.g. testing_2025-01-01_2025-12-31
│       ├── testing_<testing period>
│       │   │     # the hyper-parameter used in the testing process
│       │   ├── testing_hyper_parameter.json
│       │   │     # the performance in the testing process
│       │   │     ## e.g. testing_performance_gen0_elite0.json
│       │   └── testing_performance_gen<generation number>_elite<elite number>.json
│       │    # a folder storing the validation performance
│       ├── validation
│       │        # the validation result
│       │        ## e.g. validation_performance_gen0_elite0.json
│       │        ## is the validation result of the fittest in the first generation
│       └────── validation_performance_gen<generation number>_elite<elite number>.json
│    # a folder storing financial data in pickle format
├── pickle/
│    # a folder storing all unit test code
├── tests/
│   │   # the unit tests for the respective python files
│   ├── test_api_fin_data.py
│   ├── test_file_mgt.py
│   ├── test_ga.py
│   ├── test_genome.py
│   ├── test_population.py
│   ├── test_simulation.py
│   ├── test_strategy.py
│   └── test_validation.py
│     # Files for Git to ignore
├── .gitignore
│     # the code for information retrieval
├── api_fin_data.py
│     # the code for file management
├── file_mgt.py
│     # the code for genetic algorithm
├── ga.py
│     # the code for genes and genome to generate investment strategies
├── genome.py
│     # the code for building population, fitmap, and parents selection
├── population.py
│     # the code for running the training and validation of the GA
├── run_ga_find_fittest.py
│     # the code to test the fittest strategies in each generation on testing data
├── run_test_performance.py
│     # the code to run the simulation of trading the stocks
├── simulation.py
│     # the code to run the investment strategies
├── strategy.py
│     # the code to run validation and testing
├── validation.py
│     # the readme file
└── README.md
