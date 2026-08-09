import unittest
import genome
import numpy as np

class TestGenome(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(genome.Genome)

        g=genome.Genome()
        self.assertIsNotNone(g.get_random_gene)
        self.assertIsNotNone(g.get_gene_spec)
        self.assertIsNotNone(g.get_gdict)

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
                self.assertTrue((str(type(g.get_gene_spec()[k][k_in_k[0]])) == "<class 'float'>") or 
                                (str(type(g.get_gene_spec()[k][k_in_k[0]])) == "<class 'int'>"))
                self.assertTrue(str(type(g.get_gene_spec()[k][k_in_k[1]])) == "<class 'int'>" or str(type(g.get_gene_spec()[k][k_in_k[1]])) == "<class 'float'>")

    '''
    # test if the crossover function correctly or not
    def testCrossover(self):
        g1 = [[1], [2], [3]]
        g2 = [[4], [5], [6]]
        for i in range(10):
            g3 = genome.Genome.crossover(g1, g2)
            self.assertEqual(len(g3), 3)

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

    # test crossover()
    # test if the crossover function correctly or not
    def test_crossover(self):
        g1 = [0.41684458076790454,0.10875892671121401,0.21015362933288906]
        g2 = [0.9673206235152458,0.3214349586795838,0.8725435279202182]
        for i in range(10):
            g3 = genome.Genome.crossover(g1, g2)
            self.assertEqual(len(g3), 3)

    '''
    # test if the gene mutated or not
    def test_point(self):
        g1 = np.array([[1.0], [2.0], [3.0]])
        g2 = genome.Genome.point_mutate(g1, rate=1, amount=0.25)
        self.assertFalse(np.array_equal(g1, g2))

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

    # test point_mutate()
    ## test if the gene mutated or not
    def test_point(self):
        g1 = [0.41684458076790454,0.10875892671121401,0.21015362933288906]
        g2 = genome.Genome.point_mutate(g1, rate=1, amount=0.25)
        self.assertFalse(np.array_equal(g1, g2))

    '''
    # test if the point range is correct or not
        def test_point_range(self):
            g1 = np.array([[1.0], [0.0], [1.0], [0.0]])
            for i in range(100):
                g2 = genome.Genome.point_mutate(g1, rate=1, amount=0.25)
                self.assertLessEqual(np.max(g2), 1.0)
                self.assertGreaterEqual(np.min(g2), 0.0)

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

    ## test if the point range is correct or not
    def test_point_range(self):
        g1 = [0.41684458076790454,0.10875892671121401,0.21015362933288906]
        for i in range(100):
            g2 = genome.Genome.point_mutate(g1, rate=1, amount=0.25)
            self.assertLessEqual(np.max(g2), 1.0)
            self.assertGreaterEqual(np.min(g2), 0.0)
