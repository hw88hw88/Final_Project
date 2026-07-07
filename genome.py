# Although some of the code was adapted from my previous assignment, the code was still written following the three laws of test-driven development
import numpy as np
import json

class Genome:
    '''
    @staticmethod
    def get_random_gene(gene_length):
        # I simplified the code by eliminating the for-loop and the variable gene, and by calling numpy.random.rand()
        ## generate random number [0, 1), 0 is inclusive, but 1 is excluded
        ## Reference: https://numpy.org/doc/stable/reference/random/generated/numpy.random.rand.html
        return np.random.rand(gene_length)
    
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
    # generate a random float
    # Input: None
    # Output: 
    ## 1. a random float [0, 1), 0 is inclusive, but 1 is excluded
    @staticmethod
    def get_random_gene(gene_length):
        ## generate random number [0, 1), 0 is inclusive, but 1 is excluded
        ## Reference: https://numpy.org/doc/stable/reference/random/generated/numpy.random.rand.html
        # return a random float from 0 to 1, 1 is excluded.
        return np.random.rand(gene_length)
    
    '''
    @staticmethod
        def get_gene_spec():
            gene_spec =  {
                # I added the lower and upper limit to the features below
                # I used lower and upper limit to control the features of creatures
                ## The "scale" attributes below were removed.
                ## <=0.33 cylinder; >0.33 and <=0.66 sphere; >0.66 box
                "link-shape":{"low_limit": 0, "up_limit": 1},
                # "link-length" and "link-radius" are for cylinder tag(s)
                # "link-radius" is for sphere tag(s)
                ## Default "link-length" is 2
                "link-length": {"low_limit": 0.1, "up_limit": 2},            
                ## Default "link-radius" is 1
                "link-radius": {"low_limit": 0.1, "up_limit": 1},
                # I added "link-width", "link-height", "link-depth" for box tag(s)
                "link-width": {"low_limit": 0.1, "up_limit": 2},
                "link-depth": {"low_limit": 0.1, "up_limit": 2},
                "link-height": {"low_limit": 0.1, "up_limit": 2},
                # Default "link-recurrence" is 3
                "link-recurrence": {"low_limit": 0, "up_limit": 2},
                "link-mass": {"low_limit": 0.1, "up_limit": 1},
                # I added the scale for "link-color"
                "link-color": {"low_limit": 0, "up_limit": 1},
                ## <=0.33 revolute; >0.33 and <=0.66 continous; >0.66 fixed
                ## Default: revolute
                "joint-type": {"low_limit": 0, "up_limit": 1},
                # The range of joint-parent must be 0-1, otherwise out-of-range
                "joint-parent":{"low_limit": 0, "up_limit": 1},
                ## <=0.33 100, >0.33 and <=0.66 010, >0.66 001
                "joint-axis-xyz": {"low_limit": 0, "up_limit": 1},
                # I added the following scales:
                # "joint-limit-lower"
                # "joint-limit-upper"
                # "joint-limit-effort"
                # "joint-limit-velocity"
                ## the unit(s) of "joint-limit-lower" and "joint-limit-upper" are in radian
                # Normally, the joint-limit-lower should be lower than joint-limit-upper to make them effective for revolute joints. Otherwise, the limit will lose its function
                "joint-limit-lower": {"low_limit": 0, "up_limit": np.pi * 2}, # in radian
                "joint-limit-upper": {"low_limit": np.pi * 4, "up_limit": np.pi * 10}, # in radian
                "joint-limit-effort": {"low_limit": 1, "up_limit": 10},
                "joint-limit-velocity": {"low_limit": 1, "up_limit": 10},
                "joint-origin-rpy-1":{"low_limit": 0, "up_limit": np.pi * 2},# in radian
                "joint-origin-rpy-2":{"low_limit": 0, "up_limit": np.pi * 2},# in radian
                "joint-origin-rpy-3":{"low_limit": 0, "up_limit": np.pi * 2},# in radian
                # Default of "joint-origin-xyz-1" is 0-1
                "joint-origin-xyz-1":{"low_limit": -1, "up_limit": 1},
                "joint-origin-xyz-2":{"low_limit": -1, "up_limit": 1},
                "joint-origin-xyz-3":{"low_limit": -1, "up_limit": 1},
                # I added joint-friction
                "joint-friction":{"low_limit": 1000.0, "up_limit": 5000.0},
                # <=0.33: PULSE; <=0.66: SINE; >0.66 RAMP
                "control-waveform":{"low_limit": 0, "up_limit": 1},
                "control-amp":{"low_limit": 0.25, "up_limit": 2},
                "control-freq":{"low_limit": 0.5, "up_limit": 2},
                "control-force":{"low_limit": 500, "up_limit": 10000},
                }
            ind = 0
            for key in gene_spec.keys():
                gene_spec[key]["ind"] = ind
                ind = ind + 1
            return gene_spec

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
    # generate a dict containing the range of parameters (the range of the parameters of financial indicators)
    # Input: None
    # output:
    ## 1. a dict specifying the range of the parameters
    @staticmethod
    def get_gene_spec():
        genome_spec={
            # financial indicators:

            ## simple moving average:
            ### the range of short window of simple moving average
            'ma_short':{'low_limit': 5, 'up_limit': 15},
            ### the range of long window of simple moving average
            'ma_long':{'low_limit': 20, 'up_limit': 30},
            ### the weight of simple moving average
            'ma_weight':{'low_limit': 1, 'up_limit': 9},

            ## RSI
            ### no. of days of RSI
            'rsi_period': {'low_limit': 10, 'up_limit':20},
            ### buy the shares at RSI below 'buy_rsi'
            'buy_rsi': {'low_limit': 1, 'up_limit':30},
            ### sell the shares at RSI above 'sell_rsi'
            'sell_rsi': {'low_limit': 70, 'up_limit':99},
            ### the weight of RSI
            'rsi_weight':{'low_limit': 1, 'up_limit': 9},

            # risk management rules:
            ## sell the shares when the loss is above 'stop_loss'
            'stop_loss': {'low_limit': 3, 'up_limit':10},
            ## sell the shares when the profit is above 'take_profit'
            'take_profit': {'low_limit': 5, 'up_limit':200},

            # total no. of stocks in the investment portfolio
            'num_of_stock':{'low_limit': 1, 'up_limit':10},
            }
        return genome_spec
    
    '''
    @staticmethod
    def get_gene_dict(gene, spec):
        # initialize gdict
        gdict = {}
        for key in spec:
            ind = spec[key]["ind"]
            # I scaled the random gene in the range of lower and upper limit,
            # to generate gdict,
            # if spec[key]["up_limit"] < spec[key]["low_limit"], I will treat the upper limit as lower limit, and the lower limit as upper limit
            if spec[key]["up_limit"] >= spec[key]["low_limit"]:
                gene_range = spec[key]["up_limit"] - spec[key]["low_limit"]
                gdict[key] = gene[ind] * gene_range + spec[key]["low_limit"]
            else:
                # treating the upper limit as lower limit, and the lower limit as upper limit here
                gene_range = spec[key]["low_limit"] - spec[key]["up_limit"]            
                gdict[key] = gene[ind] * gene_range + spec[key]["up_limit"]
        return gdict

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

    # generate gdict{} according to the spec
    # input: 
    ## 1. gene,
    ## 2. genome spec
    # output: 
    ## 1. gdict{}
    @staticmethod
    def get_gdict(gene, spec):
        # initialize gdict
        gdict = {}
        ind = 0
        for key in spec:
            # if spec[key]["up_limit"] < spec[key]["low_limit"], I will treat the upper limit as lower limit, and the lower limit as upper limit
            if spec[key]["up_limit"] >= spec[key]["low_limit"]:
                gene_range = spec[key]["up_limit"] - spec[key]["low_limit"]
                gdict[key] = gene[ind] * gene_range + spec[key]["low_limit"]
            else:
                # treating the upper limit as lower limit, and the lower limit as upper limit here
                gene_range = spec[key]["low_limit"] - spec[key]["up_limit"]            
                gdict[key] = gene[ind] * gene_range + spec[key]["up_limit"]
            ind += 1
            gdict[key] = int(np.round(gdict[key], 0))
        return gdict

    @staticmethod
    def write_to_json(content, filename):
        to_json_content = json.dumps(content)
        with open(filename, 'w') as f:
            f.write(to_json_content)