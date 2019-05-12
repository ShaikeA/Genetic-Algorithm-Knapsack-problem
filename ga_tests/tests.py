"""
GA Tests
"""
from ga_components.Chromosome import Chromosome
from ga_components.Gene import Gene
from ga_components.Population import Population
import random
from collections import defaultdict
import unittest

POP_SIZE = 2


class Tests(unittest.TestCase):

    def __init__(self):
        unittest.TestCase.__init__(self)
        random.seed(1)
        self.weight = 15
        self.items = defaultdict(list, {0: [6.0, 2.0], 1: [5.0, 3.0], 2: [8.0, 6.0]})
        self.items2 = defaultdict(list, {4: [2.0, 2.0], 5: [4.0, 6.0], 6: [2.0, 2.0]})
        self.items_list = [(1, 5.0, 3.0), (2, 8.0, 6.0), (0, 6.0, 2.0)]
        self.ids = [0, 1, 2]
        self.gene = Gene(1, 2, 3)
        self.chromosome = Chromosome(self.items, self.weight, log=None, testMode=True)
        self.chromosome2 = Chromosome(self.items2, self.weight, log=None, testMode=True)
        self.population = Population(self.items, self.weight, POP_SIZE, log=None, testMode=True)

    def run_all_tests(self):
        # Gene
        self.test_get_vals()

        # Chromosome
        self.test_create_random_chromosome()
        self.test_all_genes_vals()
        self.test_get_weight()
        self.test_chrom_correction()
        self.test_genes_from_ids()
        self.test_mutate()
        self.test_crossover()
        self.test_pop_random()

        # Population
        self.test_create_initial_pop()
        self.test_calc_fitness()
        self.test_apply_mutations()
        self.test_elitism()
        self.test_new_generation()
        self.test_evolution()

    def test_get_vals(self):
        assert self.gene.get_vals() == (1, 2, 3)

    def test_create_random_chromosome(self):
        self.chromosome.create_random_chromosome()
        self.chromosome2.create_random_chromosome()

        assert self.chromosome != []
        assert self.chromosome.fitness == 19
        assert all(x in self.chromosome.ids for x in self.ids)
        assert self.chromosome.unused_ids == [ind for ind in self.items.keys() if ind not in self.ids]

    def test_all_genes_vals(self):
        assert all(x in self.items_list for x in self.chromosome.all_genes_vals())

    def test_get_weight(self):
        assert self.chromosome.get_weight() == 11

    def test_genes_from_ids(self):
        assert self.chromosome.genes_from_ids(ids=[1])[0].get_vals() == (1, 5.0, 3.0)

    def test_mutate(self):
        self.items[10] = [11.0, 1.0]
        self.items_list.append((10, 11.0, 1.0))
        self.ids.append(10)
        self.chromosome.unused_ids = [10]
        self.chromosome.mutate()
        assert (10.0, 11.0, 1.0) in self.chromosome.all_genes_vals()

    def test_crossover(self):
        child_a, child_b = self.chromosome.crossover(self.chromosome2)
        items_chromosom_1 = self.chromosome.all_genes_vals()
        items_chromosom_2 = self.chromosome2.all_genes_vals()
        assert any(x in items_chromosom_1 for x in child_a.all_genes_vals())
        assert any(x in items_chromosom_2 for x in child_a.all_genes_vals())
        assert any(x in items_chromosom_1 for x in child_b.all_genes_vals())
        assert any(x in items_chromosom_2 for x in child_b.all_genes_vals())

    def test_chrom_correction(self):
        self.chromosome.chrom_correction()
        assert self.chromosome != []
        assert self.chromosome.fitness == 19
        assert all(x in self.chromosome.ids for x in self.ids)
        assert self.chromosome.unused_ids == [ind for ind in self.items.keys() if ind not in self.ids]

    def test_pop_random(self):
        self.chromosome.pop_random()
        assert len(self.chromosome.all_genes_vals()) < 3

    # Population
    def test_create_initial_pop(self):
        self.population.create_initial_pop()
        assert len(self.population.population) == 2
        assert all(x in self.items_list for x in self.population.population[0].all_genes_vals())
        assert all(x in self.items_list for x in self.population.population[1].all_genes_vals())

    def test_calc_fitness(self):
        self.population.calc_fitness()
        assert self.population.fitness == [30, 30]

    def test_apply_mutations(self):
        """
        This function just calls the mutate (tested above) for each chromosome.
        :return:
        """
        pass

    def test_elitism(self):
        self.population.elitism(2)
        assert all(x in self.ids for x in self.population.elite[0].ids)
        assert all(x in self.ids for x in self.population.elite[1].ids)
        assert self.population.fitness_across_generations == [30]

    def test_new_generation(self):
        self.population.new_generation(select_elite=1)

        # Checking that new_pop has now 2 chromosomes. All other proceducres were tested above.
        assert len(self.population.new_pop) == POP_SIZE

    def test_evolution(self):
        self.population.evolution(select_elite=1, num_generations=2)
        self.population.fitness_across_generations
