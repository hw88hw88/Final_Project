import unittest
import genome
import os
import json

class TestGenome(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(genome.Genome)

        g=genome.Genome()
        self.assertIsNotNone(g.get_random_gene)
        self.assertIsNotNone(g.get_gene_spec)
        self.assertIsNotNone(g.get_gdict)
        self.assertIsNotNone(g.to_json)

    # test if functions return something
    def test_function_returns(self):
        g=genome.Genome()
        self.assertIsNotNone(g.get_random_gene(len(g.get_gene_spec())))
        self.assertIsNotNone(g.get_gene_spec())
        self.assertIsNotNone(g.get_gdict(gene=g.get_random_gene(len(g.get_gene_spec())), 
                                         spec=g.get_gene_spec()))

    # test if the functions return correct data type
    def test_function_return_type(self):
        g=genome.Genome()
        self.assertEqual(str(type(g.get_random_gene(len(g.get_gene_spec())))), "<class 'numpy.ndarray'>")
        self.assertEqual(str(type(g.get_gene_spec())), "<class 'dict'>")
        self.assertEqual(str(type(g.get_gdict(gene=g.get_random_gene(len(g.get_gene_spec())), 
                                         spec=g.get_gene_spec()))), "<class 'dict'>")
    
    # test if the returned value is correct
    def test_function_return_value(self):
        g=genome.Genome()

        # test get_random_gene()
        ## test if no. of random gene is generated correctly
        self.assertEqual(len(g.get_random_gene(len(g.get_gene_spec()))), len(g.get_gene_spec()))
        for i in range(100):
            self.assertEqual(len(g.get_random_gene(i)), i)

        ## test if the random gene is within the range [0, 1), where 0 is inclusive, 0 is excluded
        gene100=g.get_random_gene(100)
        for i in range(len(gene100)):
            self.assertGreaterEqual(gene100[i], 0)
            self.assertLess(gene100[i], 1)

        # test get_gdict()
        ## test if length of gdict equals length of gene specification
        self.assertEqual(len(g.get_gdict(gene=g.get_random_gene(len(g.get_gene_spec())), 
                                         spec=g.get_gene_spec())), len(g.get_gene_spec()))

        ## test if the gdict is within the range
        g_spec=g.get_gene_spec()
        g_dict=g.get_gdict(gene=g.get_random_gene(len(g_spec)), spec=g_spec)
        for i in g_dict:
            if g_spec[i]['low_limit'] <= g_spec[i]['up_limit']:
                self.assertGreaterEqual(g_dict[i], g_spec[i]['low_limit'])
                self.assertLessEqual(g_dict[i], g_spec[i]['up_limit'])
            else:
                self.assertGreaterEqual(g_dict[i], g_spec[i]['up_limit'])
                self.assertLessEqual(g_dict[i], g_spec[i]['low_limit'])
    
    # test get_gene_spec()
    def test_gene_spec(self):
        ## test if low_limit and up_limit exist in each element in gene_spec
        g=genome.Genome()
        if len(g.get_gene_spec()) > 0:
            key=list(g.get_gene_spec().keys())
            for k in key:
                # check if there are 2 elements in each element in gene_spec
                self.assertEqual(len(g.get_gene_spec()[k]), 2)
                k_in_k=list(g.get_gene_spec()[k].keys())
                ## test if low_limit and up_limit exist in each element in gene_spec
                self.assertEqual(k_in_k[0], 'low_limit')
                self.assertEqual(k_in_k[1], 'up_limit')
                # check if the value of the 2 element are integers
                self.assertEqual(str(type(g.get_gene_spec()[k][k_in_k[0]])), "<class 'int'>")
                self.assertEqual(str(type(g.get_gene_spec()[k][k_in_k[1]])), "<class 'int'>")

    # test if json file can be created successfully
    def test_to_json(self):
        g=genome.Genome()
        filename='JSON/test.json'
        content='test content'
        self.assertIsNone(g.to_json(content=content, filename=filename))
        self.assertTrue(os.path.exists(filename))
        with open(filename) as f:
            file_content=f.read()
        self.assertEqual(json.loads(file_content), content)
        os.remove(filename)

unittest.main()
