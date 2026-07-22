import genome
import os
import json
import numpy as np
import population
import simulation
import strategy
import copy
import uuid
import file_mgt

class GA:
    '''
    # the parameters of the GA, and their default values
        def __init__(self,
                    cr_start_pos,
                    cr_start_ori,
                    pool_size,
                    pop_size=200, 
                    gene_count=3,
                    min_gene=1,
                    cr_lifetime=2400, 
                    num_of_generations=1000, 
                    point_mutate_rate=0.1, 
                    point_mutate_amt=0.25,
                    shrink_mutate_rate=0.25, 
                    grow_mutate_rate=0.1, 
                    is_grow_legs_only=False, 
                    max_gene_to_grow=300,
                    is_handcrafted_urdf=False):
            # user input pool size
            self.pool_size=pool_size
            self.pop_size=pop_size
            # make sure the gene_count is at least 4 for the 4 wheels of the handcrafted robot
            if gene_count < min_gene:
                self.gene_count=min_gene
            else:
                self.gene_count=gene_count
            self.min_gene=min_gene
            self.JSON_filename='JSON/genome_spec.json'
            self.log_filename='JSON/log_ga.json'
            # the lifetime of creature(s) in number of frames
            self.cr_lifetime=cr_lifetime
            # the number of generations
            self.num_of_generations=num_of_generations
            self.point_mutate_rate=point_mutate_rate
            self.point_mutate_amt=point_mutate_amt
            self.shrink_mutate_rate=shrink_mutate_rate
            self.grow_mutate_rate=grow_mutate_rate
            self.is_grow_legs_only=is_grow_legs_only
            self.max_gene_to_grow=max_gene_to_grow
            self.cr_start_pos=cr_start_pos
            self.cr_start_ori=cr_start_ori
            self.is_handcrafted_urdf=is_handcrafted_urdf

            # save the parameters to JSON
            to_json_content = {
                'cr_start_pos': self.cr_start_pos,
                'cr_start_ori': self.cr_start_ori,
                'pop_size': self.pop_size,
                'gene_count': self.gene_count,
                'cr_lifetime': self.cr_lifetime,
                'num_of_generations': self.cr_lifetime,
                'point_mutate_rate': self.point_mutate_rate,
                'point_mutate_amt': self.point_mutate_amt,
                'shrink_mutate_rate': self.shrink_mutate_rate,
                'grow_mutate_rate': self.grow_mutate_rate,
                'is_grow_legs_only': self.is_grow_legs_only,
                'max_gene_to_grow': self.max_gene_to_grow,
                "is_handcrafted_urdf": self.is_handcrafted_urdf,
            }
            genome.Genome.to_json(to_json_content, 'JSON/config.json')

            # save the genome spec to JSON
            genome.Genome.to_json(genome.Genome.get_gene_spec(), self.JSON_filename)

            # remove the old log file
            if os.path.exists(self.log_filename):
                os.remove(self.log_filename)

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
    # the parameters of the GA, and their default values
    def __init__(
        self,
        pool_size,
        start_up_cash,
        trading_fee,
        pop_size=50,
        num_of_generations=50,
        point_mutate_rate=0.1, 
        point_mutate_amt=0.25,
        fin_start=None,
        fin_end=None,
    ):
        self.pool_size=pool_size
        self.fin_start=fin_start
        self.fin_end=fin_end
        self.start_up_cash=start_up_cash
        self.trading_fee=trading_fee
        self.pop_size=pop_size
        self.gene_spec_filename='JSON/gene_spec.json'
        self.ga_performance_filename='JSON/ga_performance.json'
        self.hyper_parameter_filename = 'JSON/hyper_parameter.json'
        self.elite_json_filename = 'JSON/fittest'
        self.elite_csv_filename = 'CSV/fittest'

        # the number of generations
        self.num_of_generations=num_of_generations
        self.point_mutate_rate=point_mutate_rate
        self.point_mutate_amt=point_mutate_amt

        # store the fittest strategies
        self.fittest_st = []

        # number of fittest strategies to be selected to the next generation
        ## e.g. 3 means the 3 fittest strategies of the current and previous generations will be saved 
        ### to self.fittest_st, 
        ### to JSON file(s), 
        ### to CSV file(s), and
        ### to next generation
        self.num_of_elite = 3

        # remove old files
        ## remove the files in JSON folder
        files = file_mgt.FileMgt.list_files_in_directory('JSON')
        for file in files:
            os.remove(file)

        ## remove old elite or fittest CSV files
        for p in os.listdir(self.elite_csv_filename):
            os.remove(self.elite_csv_filename + '/' + p)

        # run id
        ## to identify the files generated this time
        self.run_id = str(uuid.uuid4())

        # save the hyper-parameters to JSON
        save_hyper_parameter_to_json_content = {
            'run_id': self.run_id,
            'pop_size': self.pop_size,
            'num_of_generations': self.num_of_generations,
            'point_mutate_rate': self.point_mutate_rate,
            'point_mutate_amt': self.point_mutate_amt,
            'start_up_cash': self.start_up_cash,
            'fin_start': self.fin_start,
            'fin_end': self.fin_end,
            'trading_fee': self.trading_fee,
            'pool_size': self.pool_size,
        }
        file_mgt.FileMgt.write_to_json(to_json_content=save_hyper_parameter_to_json_content, filename=self.hyper_parameter_filename)

        # save the genome spec to JSON
        gene_spec = genome.Genome.get_gene_spec()
        gene_spec['run_id'] = str(self.run_id)
        file_mgt.FileMgt.write_to_json(to_json_content=gene_spec, filename=self.gene_spec_filename)

        # store log file content
        self.ga_performance_file_content = ''

    '''
    # calculating and printing the matrics
    def matrics(self, pop, generation):
        # the performance of creatures
        max_closeness = []
        links = []
        distance_travelled = []
        total_movement = []
        rewards = []
        for cr in pop.creatures:
            max_closeness.append(cr.get_max_closeness())
            links.append(len(cr.get_expanded_links()))
            distance_travelled.append(cr.get_distance_travelled())
            total_movement.append(cr.get_total_movement())
            rewards.append(cr.get_reward())

        # for the fittest creature
        fittest_reward = np.max(rewards)
        for cr in pop.creatures:
            if cr.get_reward() == fittest_reward:
                # get the max closeness of the fittest creature
                fittest_closeness = cr.get_max_closeness()
                fittest_links = len(cr.get_expanded_links())
                fittest_travelled = cr.get_distance_travelled()
                fittest_total_movement = cr.get_total_movement()
                break

        # prepare the information to be printed and returned
        log = {
            # the shortest distance of max closeness among creatures
            'max_closeness': str(np.round(np.min(max_closeness), 3)),
            # the mean distance of max closeness among creatures
            'mean_closeness': str(np.round(np.mean(max_closeness), 3)),
            # the longest distance of max closeness among creatures
            'min_closeness':str(np.round(np.max(max_closeness), 3)), 
            'mean_links':str(np.round(np.mean(links))),
            'max_links':str(np.round(np.max(links))),
            'min_links':str(np.round(np.min(links))),
            'pop_size':str(len(pop.creatures)),
            'max_dist_travelled':str(np.round(np.max(distance_travelled), 3)),
            'min_dist_travelled':str(np.round(np.min(distance_travelled), 3)),
            'max_total_movement':str(np.round(np.max(total_movement), 3)),
            'min_total_movement':str(np.round(np.min(total_movement), 3)),
            'max_reward':str(np.round(np.max(rewards), 3)),
            'min_reward':str(np.round(np.min(rewards), 3)),
            # the max closeness of the fittest creature (the creature with highest reward)
            'fittest_closeness':str(np.round(fittest_closeness, 3)),
            'fittest_links':str(np.round(fittest_links, 3)),
            'fittest_travelled':str(np.round(fittest_travelled, 3)),
            'fittest_total_movement':str(np.round(fittest_total_movement, 3)),
        }

        print(generation,
            "max closeness:", log['max_closeness'], 
            ", mean:", log['mean_closeness'], 
            ", mean links:", log['mean_links'], 
            ", max links:", log['max_links'],
            ", pop size:", log['pop_size'],
            ", dist travelled (max):", log['max_dist_travelled'],
            ", (min):", log['min_dist_travelled'],
            ", total dist (max):", log['max_total_movement'],
            ", (min):", log['min_total_movement'],
            ", reward (max):", log['max_reward'],
            ", (min):", log['min_reward'],
            ", fittest closeness:", np.round(fittest_closeness, 3))
        
        # saving the above information to csv log file
        with open(self.log_filename, "a") as f:
            f.write(json.dumps(log))
            f.write(',\n')
            
        return rewards
    
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
    # calculating and printing the matrics
    # input:
    # 1. generation: number of generations. 1 stands for the first generation
    # output: no returned value
    # change:
    # 1. add content to ga_performance_file_content
    # 2. print the matrics and performance
    def matrics(self, generation):
        # find the fittest strategy, and log and print its performance
        rewards = [st.rewards for st in self.fittest_st]
        best_fit_reward = np.max(rewards)

        for st in self.fittest_st:
            if st.rewards == best_fit_reward:
                fittest_st = st
                break

        # prepare the information to be printed and returned
        log = {
            "generation": str(generation),
            "max_reward":str(np.round(np.max(rewards), 3)),
            "min_reward":str(np.round(np.min(rewards), 3)),
            # the highest reward strategy
            "fittest gdict": fittest_st.gdict,
            "fin_start": self.fin_start,
            "fin_end": self.fin_end,
            "fittest return": fittest_st.cumulative_return,
            "fittest value": fittest_st.total_value,
            "fittest max drawdown": fittest_st.max_drawdown,
            "fittest win rate": np.round((fittest_st.num_of_increase_in_value / fittest_st.age), 3),
        }

        print(generation,
            'max_reward: ',str(np.round(np.max(rewards), 3)),
            'min_reward: ',str(np.round(np.min(rewards), 3)),
            "fittest return:", fittest_st.cumulative_return,
            "fittest value:", fittest_st.total_value,
            )

        # saving the above information to JSON log file
        self.ga_performance_file_content += json.dumps(log) + ',\n'

    '''
    # passing the fittest creature on to the next generation
    @staticmethod
    def elitism(reward, pop, new_creatures, generation):
        # elitism
        best_fit_reward = np.max(reward)
        for c_in_pop in pop.creatures:
            if c_in_pop.get_reward() == best_fit_reward:
                # deepcopy to copy the fittest creature
                fittest = copy.deepcopy(c_in_pop)
                # Reset all parameters, but leaving the DNA unchanged
                fittest.reset()
                # I appended the fittest creature to new_creatures, instead of assign it to the first element of new_creatures. This can keep both the fittest creature and all newly breeded creatures for the next generation
                new_creatures.append(fittest)

                # saving the fittest to CSV file
                filename = "CSV/elite_"+str(generation)+".csv"
                genome.Genome.to_csv(c_in_pop.dna, filename)
                # stop iteration after the fittest was found
                break
        return new_creatures

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
    # saving the fittest strategies to or updating <self.fittest_st>
    # saving the fittest strategies to CSV and JSON files
    # input:
    # 1. pop: the population instance
    # 2. genereation: the generation number, such as 1 stands for the first generation
    # output: no returned value
    # change:
    # 1. JSON file(s) storing gdict of the <self.num_of_elite> fittest
    # 2. CSV file(s) storing the genome of the <self.num_of_elite> fittest
    # 3. update the self.fittest_st
    def elitism(self, pop, generation):
        # the performance of strategies in current generation
        rewards = copy.deepcopy([st.rewards for st in pop.strategies])

        # elitism
        # find the <self.num_of_elite> fittest strategy in population of current generation
        rewards.sort(reverse = True)
        fittest_rewards = rewards[: self.num_of_elite]

        # store the <self.num_of_elite> fittest strategies in the population of current generation
        fittest_st = []

        # find the <self.num_of_elite> fittest strategies in the population of current generation
        for st in pop.strategies:
            for new_fit in range(len(fittest_rewards)):
                if st.rewards == fittest_rewards[new_fit]:
                    # append the <self.num_of_elite> fittest strategies
                    fittest_st.append(st)
                    # remove the reward after appending the strategy
                    ## for speeding up the searching
                    fittest_rewards.pop(new_fit)
                    break
            if len(fittest_st) == self.num_of_elite:
                break

        # appending all fittest strategies from previous generation
        for old_st in self.fittest_st:
            fittest_st.append(old_st)

        # store the rewards of the fittest strategies
        new_fittest_rewards = [all_st.rewards for all_st in fittest_st]

        # sorting the rewards in descending order
        new_fittest_rewards.sort(reverse=True)

        # leave the first <self.num_of_elite> fittest
        new_fittest_rewards = new_fittest_rewards[: self.num_of_elite]

        # store the new fittest strategies
        new_fittest_st = []
        # find the <self.num_of_elite> fittest from the new fittest strategies
        for st in fittest_st:
            for r in new_fittest_rewards:
                if st.rewards == r:
                    new_fittest_st.append(st)
                    break

        # save the new fittest
        self.fittest_st = new_fittest_st

        # saving the fittest to files
        for st in range(len(new_fittest_st)):
            # saving the fittest DNA to CSV file
            dna_filename = self.elite_csv_filename + '/elite_' + str(st) + '_gen'+str(generation)+'.csv'
            gene=copy.deepcopy(new_fittest_st[st].gene)
            gene=np.append(gene, self.run_id)
            file_mgt.FileMgt.write_list_to_csv(list_content=gene, csv_file_path=dna_filename)
            # saving the fittest gdict to JSON file
            gdict_filename = self.elite_json_filename + '/elite_' + str(st) + '_gen'+str(generation)+'.json'
            gdict=copy.deepcopy(new_fittest_st[st].gdict)
            gdict['run_id'] = self.run_id
            gdict['rewards'] = new_fittest_st[st].rewards
            file_mgt.FileMgt.write_to_json(to_json_content=gdict, filename=gdict_filename)

    '''
    # the main body and workflow of GA
    def run_ga(self):
        # checking user input: pool size
        if self.pool_size is None or type(self.pool_size) is not int:
            # prompt users to input number of thread(s)
            self.user_input()

        pop = population.Population(pop_size=self.pop_size, 
                                    gene_count=self.gene_count)

        # determine the number of threads based on user input
        if self.pool_size > 1:
            sim = simulation.ThreadedSim(pool_size=self.pool_size, cr_start_pos=self.cr_start_pos, cr_start_ori=self.cr_start_ori, is_handcrafted_urdf=self.is_handcrafted_urdf)
            print('Multi-threads:', self.pool_size)
        else:
            sim = simulation.Simulation(cr_start_pos=self.cr_start_pos, cr_start_ori=self.cr_start_ori, is_handcrafted_urdf=self.is_handcrafted_urdf)
            print('Single thread')

        # preparing the JSON log file at the beginning
        with open(self.log_filename, "w") as f:
            f.write('{"result":[')

        for generation in range(self.num_of_generations):
            if self.pool_size > 1:
                # multi-threads version
                sim.eval_population(pop, self.cr_lifetime)
            else:
                # single-thread version 
                # where we just call run_creature instead
                # of eval_population
                for cr in pop.creatures:
                    sim.run_creature(cr=cr, cr_lifetime=self.cr_lifetime)

            rewards = self.matrics(pop=pop, generation=generation)

            fit_map = population.Population.get_fitness_map(reward=rewards)
            new_creatures = []
            # I changed the number of newly breeded creatures to existing number minus 1, because the current fittest creature will be appended. The population size remains unchanged.
            # breeding new creatures
            for i in range(len(pop.creatures) - 1):
                p1_ind = population.Population.select_parent(fit_map)
                p2_ind = population.Population.select_parent(fit_map)
                p1 = pop.creatures[p1_ind]
                p2 = pop.creatures[p2_ind]
                # now we have the parents!

                dna = genome.Genome.crossover(g1=p1.dna, g2=p2.dna)
                dna = genome.Genome.point_mutate(dna, rate=self.point_mutate_rate, amount=self.point_mutate_amt)
                dna = genome.Genome.shrink_mutate(dna, rate=self.shrink_mutate_rate)
                # The if-statement here was added after the experiments to fix the bug of the failed sim because of too many links
                # limit the number of links to grow
                if len(p1.get_expanded_links()) <= self.max_gene_to_grow and len(p2.get_expanded_links()) <= self.max_gene_to_grow:
                    # I added the parameter 'max_gene' to grow_mutate(). Genome will not grow, once the max number of genes has been reached.
                    while True:
                        # keep growing, until the number of genes reaches the minimum number
                        ## avoid error(s) for handcrafted robot(s)
                        if len(dna) >= self.min_gene:
                            break
                        dna = genome.Genome.grow_mutate(dna, rate=1.0, max_gene_to_grow=self.max_gene_to_grow)
                    dna = genome.Genome.grow_mutate(dna, rate=self.grow_mutate_rate, max_gene_to_grow=self.max_gene_to_grow)
                new_cr = creature.Creature(gene_count=self.gene_count, dna=dna, is_grow_legs_only = self.is_grow_legs_only)
                new_creatures.append(new_cr)
                # I added the assertion to assert at least 1 creature in new_creatures
                assert len(new_creatures) >= 1
            
            # elitism
            new_creatures = self.elitism(reward=rewards, pop=pop, new_creatures=new_creatures, generation=generation)
            # Assigning the new creatures and the fittest to the population for the next generation
            pop.creatures = new_creatures

        # closing the JSON log file at the end
        with open(self.log_filename, "a") as f:
            f.write(']}')

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
    # the main body and workflow of GA
    # input: None
    # Output: No returned value
    # Changes:
    # 1. write the log of strategy performance to self.ga_performance_filename
    # 2. run simulation
    # 3. call fitmap
    # 4. breed new strategies
    def run_ga(self):
        pop = population.Population(pop_size=self.pop_size, start_up_cash=self.start_up_cash)

        # determine the number of threads based on user input
        if self.pool_size > 1:
            sim_t = simulation.ThreadedSim(
                pool_size=self.pool_size, 
                fin_start=self.fin_start,
                fin_end=self.fin_end,
                trading_fee=self.trading_fee)
            print('Multi-threads:', self.pool_size)
        else:
            sim = simulation.Simulation(
                fin_start=self.fin_start,
                fin_end=self.fin_end,
                trading_fee=self.trading_fee)
            print('Single thread')

        # preparing the JSON log file at the beginning
        self.ga_performance_file_content = '{"run_id": "' + self.run_id + '",\n "result":[\n'

        for generation in range(self.num_of_generations):
            if self.pool_size > 1:
                # multi-threads version
                sim_t.eval_population(pop=pop)
            else:
                # single-thread version 
                for st in pop.strategies:
                    sim.run_strategy(st=st)

            # elitism
            ## finds the <self.num_of_elite> fittest from current and previous generations
            new_strategies = self.elitism(
                pop=pop, 
                generation=generation)

            # calculating, logging and printing matrics of the fittest strategy
            ## it must be called after the elitism, because the self.elitism finds the fittest from current and previous generations
            self.matrics(generation=generation)

            # getting the fitmap for breeding
            fit_map = population.Population.get_fitness_map(reward=[st.rewards for st in pop.strategies])

            # adding the 3 fittest strategies to the next generation
            new_strategies = copy.deepcopy(self.fittest_st)

            # the number of newly breeded strategies is the existing number of strategies minus <len(new_strategies)>, because the <len(new_strategies)> fittest strategies were added. The population size remains unchanged.
            # breeding new strategies
            for i in range(len(pop.strategies) - len(new_strategies)):
                p1_ind = population.Population.select_parent(fit_map)
                p2_ind = population.Population.select_parent(fit_map)
                p1 = pop.strategies[p1_ind]
                p2 = pop.strategies[p2_ind]
                # now we have the parents!

                dna = genome.Genome.crossover(g1=p1.gene, g2=p2.gene)
                dna = genome.Genome.point_mutate(dna, rate=self.point_mutate_rate, amount=self.point_mutate_amt)
                new_st = strategy.Strategy(start_up_cash=self.start_up_cash, gene=dna)

                new_strategies.append(new_st)


            # Assigning the new strategies and the fittest to the population for the next generation
            pop.strategies = new_strategies

        # saving log content to the JSON log file at the end
        self.ga_performance_file_content = self.ga_performance_file_content[:-2]
        self.ga_performance_file_content += '\n]}'
        with open(self.ga_performance_filename, "w") as f:
            f.write(self.ga_performance_file_content)
