import unittest
import os
import json
import file_mgt

class TestFileMgt(unittest.TestCase):
    # test write_to_json()
    def test_write_to_json(self):
        fm=file_mgt.FileMgt()
        to_json_content='test content'
        filename='JSON/test.json'

        fm.write_to_json(to_json_content=to_json_content, filename=filename)

        self.assertTrue(os.path.exists(filename))
        with open(filename) as f:
            content=f.read()
            content=json.loads(content)
        self.assertEqual(content, to_json_content)
        os.remove(filename)

    # test write_list_to_csv()
    def test_write_list_to_csv(self):
        fm=file_mgt.FileMgt()
        dna_list=[1.234, 2.345, 3.567]
        csv_file='CSV/test.csv'
        fm.write_list_to_csv(list_content=dna_list, csv_file_path=csv_file)

        self.assertTrue(os.path.exists(csv_file))

        with open(csv_file) as f:
            csv_str = f.read()
            lines = csv_str[:-1]
            file_items = lines.split(',')
            items_from_file=[float(item) for item in file_items]
        self.assertEqual(items_from_file, dna_list)
        os.remove(csv_file)

    # test list_files_in_directory()
    def test_list_files_in_directory(self):
        pass

unittest.main()