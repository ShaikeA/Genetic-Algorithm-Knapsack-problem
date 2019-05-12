"""
The Population class
"""
import numpy as np
import random
from itertools import cycle
from operator import itemgetter
import matplotlib.pyplot as plt
from ga_components.Chromosome import Chromosome


class Population:
    """
    The Population class
    """

    def __init__(self, ITEMS, max_weight, POP_SIZE, log=None, testMode=False):
        """
        The instructor of population object. It gets all items and max weight
        :param ITEMS:
        :param max_weight:
        """
        self.items = ITEMS
        self.pop_size = POP_SIZE
        self.max_weight = max_weight
        self.population = []
        self.fitness_across_generations = []
        self.log = log
        self.test = testMode

    def create_initial_pop(self):
        """
        Creates an initial population with POP_SIZE random chromosomes.
        :return:
        """
        for i in range(self.pop_size):
            ch = Chromosome(self.items, self.max_weight, self.log)
            ch.create_random_chromosome()
            self.population.append(ch)
        return self.population

    def calc_fitness(self):
        """
        Calculates the fitness of all chromosomes in the population
        :return:
        """
        self.fitness = [chrom.fitness for chrom in self.population]

    def apply_mutations(self, num_to_mutate):
        """
        Applies mutation of a random number of chromosoes from the new population
        that was just created(including the elite ones from the last population)
        :return:
        """
        random.shuffle(self.new_pop)
        for ind_chrom in range(num_to_mutate):
            self.new_pop[ind_chrom].mutate()

    def elitism(self, amount):
        """
        Finds the X (parameter) finest chromosomes of the current population
        and returns them.
        :param amount:
        :return:
        """
        # Calculating fitness of current population
        self.calc_fitness()

        # Getting indices of the [amount] elite chromosomes and saving them into self.elite
        indices_elite = list(np.array(self.fitness).argsort()[-amount:][::-1])
        self.elite = itemgetter(*indices_elite)(self.population)

        # Saving the max fit of the current population (for plotting)
        self.fitness_across_generations.append(max(self.fitness))
        return self.elite, self.fitness_across_generations

    def new_generation(self, select_elite):
        """
        Creates a new generation of population by using the crossover and
        mutation methods. The genereation has a fixed number of chromosomes which was defined prior
        to this method.
        :param select_elite: number of elite chromosomes to select in each generation
        :return:
        """
        # Shuffling the population and creating a pool
        random.shuffle(self.population)
        pop_pool = cycle(self.population)

        # Initializing the new population list
        self.new_pop = []
        ind_pop = 0

        while len(self.new_pop) < self.pop_size - select_elite:
            parent_a = next(pop_pool)
            parent_b = next(pop_pool)
            child_a, child_b = parent_a.crossover(parent_b)
            self.new_pop.extend([child_a, child_b])

        # mutation
        if self.pop_size > 2:  # This applies only for the regular run (not the tests)
            num_to_mutate = random.randint(1, self.pop_size - select_elite)
            self.apply_mutations(num_to_mutate)
            self.new_pop.extend(self.elite)
            self.population = self.new_pop
            self.elitism(select_elite)

    def evolution(self, select_elite, num_generations=200):
        """
        Generates the evolution.
        :return:
        """
        # Finds the 2 elite chromosomes and save in self.elite
        self.elitism(select_elite)

        for ind_gen in range(num_generations):
            self.new_generation(select_elite=select_elite)
            if ind_gen % 100 == 0 and self.test is False:
                text = "\nGeneration {}:\n Max score {} | Chromosome: {}\n-------------"
                self.log.logger.info(text.format(ind_gen, max(self.fitness),self.population[np.argmax(self.fitness)]
                                                 .all_genes_vals()))
        if self.test is False:
            if isinstance(self.elite, tuple):
                self.log.logger.info("\nBest chromosomes: {}".format([x.all_genes_vals() for x in self.elite]))
            else:
                self.log.logger.info("\nBest chromosome: {}".format(self.elite.all_genes_vals()))
            plt.plot(self.fitness_across_generations)
            plt.xlabel("Generations")
            plt.ylabel("Total Value")
            plt.grid()
            plt.show(block=True)
