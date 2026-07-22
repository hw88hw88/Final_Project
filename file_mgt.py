import os
import json

class FileMgt:
    # find all files in a directory, including all files in all sub-directories
    # input:
    # 1. directory: a string storing the file path
    # output:
    # 1. a list to store the file paths of all files in the directory, or
    # 2. return None, if there is no file in the directory
    @staticmethod
    def list_files_in_directory(directory):
        if os.path.exists(directory):
            files = []
            def list_files(directory):
                for f in os.listdir(directory):
                    if os.path.isfile(os.path.join(directory, f)):
                        files.append(os.path.join(directory, f))
                    else:
                        list_files(os.path.join(directory, f))
            list_files(directory)
            files.sort()
            return files
        return None

    '''
    @staticmethod
    def to_json(to_json_content, filename):
        content = json.dumps(to_json_content)
        with open(filename, 'w') as f:
            f.write(content)
    
    Title: CM3020 Artificial Intelligence, Week 10 Mid-term coursework
    Author: The author of this project (Anonoymous submission of assignment)
    Date: 2026
    Code version: N/A
    Availability: Submitted Assignment (Not published)
    (Week 10 Mid-term coursework of CM3020 Artificial Intelligence, 2026)

    The code in this function was adapted from the mid-term coursework in the week 10 of "CM3020 Artificial Intelligence" by the author of this project
    All the code was written and prepared by the author of this project, with reference to the starter code from the mid-term coursework of "CM3020 Artificial Intelligence" (Yee-King, no date)

    Reference:
    Yee-King, M., (no date) CM3020 Artificial Intelligence, Week 10 Mid-term coursework starter code [online] Available from: https://www.coursera.org/learn/uol-cm3020-artificial-intelligence/assignment-submission/6JASg/mid-term-coursework [8 December 2025]
    '''
    # write content, such as gene spec, to JSON file(s)
    # input: 
    ## 1. file path
    ## 2. JSON content in a python dict
    # output:
    ## 1. JSON file
    @staticmethod
    def write_to_json(to_json_content, filename):
        content = json.dumps(to_json_content)
        with open(filename, 'w') as f:
            f.write(content)

    '''
    @staticmethod
    def to_csv(dna, csv_file):
        csv_str = ""
        for gene in dna:
            for val in gene:
                csv_str = csv_str + str(val) + ","
            csv_str = csv_str + '\n'

        with open(csv_file, 'w') as f:
            f.write(csv_str)

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
    # Write a list of content, such as DNA, to CSV file(s)
    # input: 
    ## 1. list_content: a single dimension list
    ## 2. csv file path
    # output:
    ## 1. write CSV file to disk
    @staticmethod
    def write_list_to_csv(list_content, csv_file_path):
        csv_str = ""
        for element in list_content:
            csv_str = csv_str + str(element) + ","
        csv_str = csv_str[:-1] + '\n'

        with open(csv_file_path, 'w') as f:
            f.write(csv_str)
