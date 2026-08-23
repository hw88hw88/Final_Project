import unittest
import load_trained_strategy
import file_mgt
import os

class TestLoadTrainedStrategy(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(load_trained_strategy.LoadTrainedStrategy)

        self.assertIsNotNone(load_trained_strategy.LoadTrainedStrategy.get_run_id)

    # test get_run_id()
    def test_get_run_id(self):
        loading = load_trained_strategy.LoadTrainedStrategy()
        fm = file_mgt.FileMgt()

        # write run_id to a test file
        run_id_file_path='CSV/test_run_id.csv'
        if not fm.check_file_exist(run_id_file_path):
            fm.write_csv(csv_file_path=run_id_file_path, to_csv_content='test')

        run_id = loading.get_run_id(num_of_run=0, run_id_file_path='CSV/test_run_id.csv')

        # check the content of the run_id
        self.assertEqual(run_id, 'test')

        # remove test file
        os.remove(run_id_file_path)


