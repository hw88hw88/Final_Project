import unittest
import chatbot
import file_mgt
import genome
import os


class TestChatbot(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(chatbot.Chatbot)

    # test the get_strategy()
    def test_get_strategy(self):
        bot = chatbot.Chatbot()

        fm = file_mgt.FileMgt()
        # create a testing strategy
        g = genome.Genome()
        spec=g.get_gene_spec()
        
        test_gdict = g.get_gdict(
            gene=g.get_random_gene(gene_length=len(spec)),
            spec=spec
            )
        spec['run_id'] = str('unittest')

        # test file path
        test_run_id_file = 'CSV/unittest_run_id.csv'
        test_hyper_params_file = 'JSON/unittest_hyper_parameter.json'
        test_gdict_file = 'JSON/unittest_gdict.json'

        # create test files
        ## test_run_id file
        fm.write_csv(
            csv_file_path=test_run_id_file,
            to_csv_content='test_id'
        )

        ## test_hyper-parameters file
        fm.write_to_json(
            to_json_content={'num_of_generations': 50},
            filename=test_hyper_params_file
        )

        ## test gdict file
        fm.write_to_json(
            to_json_content=test_gdict,
            filename=test_gdict_file,
        )

        trained_strategy = bot.get_strategy(
            run_id_file_path=test_run_id_file,
            hyper_params_file_path=test_hyper_params_file,
            gdict_file_path=test_gdict_file,
        )
        self.assertEqual(trained_strategy.gdict, test_gdict)

        # remove test files
        os.remove(test_run_id_file)
        os.remove(test_hyper_params_file)
        os.remove(test_gdict_file)

    