import unittest
import strategy

class TestStrategy(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(strategy.Strategy)

        s=strategy.Strategy()
        self.assertIsNotNone(s.rewards)
        self.assertIsNotNone(s.cumulative_return)
        self.assertIsNotNone(s.stocks)
        self.assertIsNotNone(s.annual_return)
        self.assertIsNotNone(s.max_drawdown)
        self.assertIsNotNone(s.num_of_trade)

        self.assertIsNotNone(s.gdict)

        self.assertIsNotNone(s.fitness)


    # # test if functions return something
    # def test_function_returns(self):
    #     s=strategy.Strategy()
    #     self.assertIsNotNone(s.get_rewards())

unittest.main()