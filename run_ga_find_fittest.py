
'''
import ga
import sys

# start running the genetic algorithm here to start selecting the fittest creatures
# input: 
## 1. number of threads of the running environment
# output: printing some metrics of the creatures for each generation
try:
        assert len(sys.argv) == 2, "Usage: python run_ga_find_fittest.py [number of threads] \n For example (2 threads): python run_ga_find_fittest.py 2"

        # change the parameters here, if needed
        g = ga.GA(
                cr_start_pos=[6, 6, 10],
                cr_start_ori=[0, 0, 0, 1],
                pool_size = sys.argv[1], 
                pop_size=100,
                gene_count=3,
                min_gene=1,
                # if is_handcrafted_urdf = True, gene_count >= 6 for:
                ## 1. the root link, 
                ## 2. the top link and 
                ## 3. the 4 wheels
                is_handcrafted_urdf=False,
                cr_lifetime=2400, 
                num_of_generations=200,
                point_mutate_rate=0.1, 
                point_mutate_amt=0.25, 
                shrink_mutate_rate=0.25, 
                grow_mutate_rate=0.1,
                is_grow_legs_only=False,
                max_gene_to_grow=100)
        # run the genetic algorithm
        g.run_ga()

except Exception as e:
    print(e)

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

''' 
The running environment:
Host OS: WSL2.0 on Windows 11
Guest OS: Ubuntu 24.04

Python 3.12.3

'''
import ga
import sys

# start running the genetic algorithm here to start selecting the fittest creatures
# input: 
## 1. number of threads of the running environment
# output: printing some metrics of the creatures for each generation
if len(sys.argv) == 2 and type(int(sys.argv[1])) is int:
        pool_size = sys.argv[1]
else:
        pool_size = 1
        print("Usage: python run_ga_find_fittest.py [number of threads] \n For example (2 threads): python run_ga_find_fittest.py 2")
# stock ticker symbols were stored in 'CSV/stock_code.csv'
# change the parameters here, if needed
g = ga.GA(
        pool_size=int(pool_size),
        pop_size=50,
        num_of_generations=50,
        point_mutate_rate=0.1, 
        point_mutate_amt=0.25,
        fin_start="2020-01-01",
        fin_end="2020-12-31",
        start_up_cash=100000,
        # trading fee includes commission fee, trading platform fee, and other fee for each transaction of stocks
        # trading fee is per order fee (e.g. 0.01 means US$0.01 per share in the order)
        trading_fee=0.01,
)
# run the genetic algorithm
g.run_ga()


