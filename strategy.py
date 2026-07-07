import genome

class Strategy:
    def __init__(self):
        # record the performance
        self.rewards=0
        self.cumulative_return=0
        self.stocks={}
        self.annual_return=0
        self.max_drawdown=0
        self.sharpe_ratio=None
        self.win_rate=None
        self.num_of_trade=0
        
        # the configuration or structure of the strategy
        spec=genome.Genome.get_gene_spec()
        gene=genome.Genome.get_random_gene(len(spec))
        self.gdict=genome.Genome.get_gdict(
            gene=gene,
            spec=spec
        )
    
    def fitness(self):
        pass