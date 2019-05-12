"""
The chromosome class
"""
import random
from ga_components.Gene import Gene
import sys


class Chromosome:
    """
    The chromosome class
    """

    def __init__(self, items, max_weight, log=None, testMode=False):
        """
        Chromosone instructor
        :param items: a list of numpy array [(value, weight, id), (value, weight, id)...]
        """
        self.items = items
        self.unused_ids = list(self.items.keys())
        self.weight = 0
        self.chromosome = []
        self.fitness = 0
        self.ids = []
        self.max_weight = max_weight
        self.log = log
        self.test = testMode

    def create_random_chromosome(self):
        """
        Creates a random valid chromosome (random genes which their weights summation
        is less than the max weight of the knapsack
        :return:
        """
        random.shuffle(self.unused_ids)
        g_ids = []
        weight_below_max = True

        # Continue as long as we are below the max weight and that there are still unused genes
        while weight_below_max is True and self.unused_ids != []:
            random_id = self.unused_ids.pop()
            single_gene = Gene(random_id, *self.items[random_id])
            if self.weight + single_gene.weight < self.max_weight:
                self.weight += single_gene.weight
                g_ids.append(single_gene.g_id)
                self.chromosome.append(single_gene)
            else:
                continue
        self.fitness = sum([gene.get_vals()[1] for gene in self.chromosome])
        self.ids = g_ids
        self.unused_ids = [ind for ind in self.items.keys() if ind not in self.ids]
        return self.chromosome

    def all_genes_vals(self):
        """
        Returns the values of all he chromosome's genes
        :return:
        """
        return [gene.get_vals() for gene in self.chromosome]

    def get_weight(self):
        """
        Calculates the weight of a chromosome and returns it
        :return:
        """
        all_genes = self.all_genes_vals()
        return sum([gene[2] for gene in all_genes])  # faster than numpy in short lists

    def pop_random(self):
        """
        Pops out a random gene out of the chromosome
        :return:
        """
        self.chromosome.pop(random.randint(0, len(self.chromosome) - 1))

    def chrom_correction(self):
        """
        Checks if the chromosome's weight is below the total allowed weight.
        if not, it removes items (randomly)
        Also, it updates the genes' ids of the chromosome
        :return:
        """
        while self.get_weight() > self.max_weight:
            self.pop_random()

        all_genes = self.all_genes_vals()
        self.ids = [gene[0] for gene in all_genes]
        self.unused_ids = [ind for ind in self.items.keys() if ind not in self.ids]
        self.fitness = sum([gene.get_vals()[1] for gene in self.chromosome])
        if self.unused_ids == [] and self.log is not None:
            self.log.logger.info("All items can fit into the knapsack")
            sys.exit()

    def genes_from_ids(self, ids, chrom=None):
        """
        This method does 2 things:
         - gets a list of ids and returns a list of genes (chrom = None)
         - gets a list of ids and another chromosom and returns the genes which are in the chromosom.
        :param ids: list of ids
        :param chrom: a chromosone which is related to the given ids
        :return:
        """
        genes = []
        if chrom is None:
            for gene_id in ids:
                genes.append(Gene(gene_id, *self.items[gene_id]))
        else:
            for gene in chrom:
                if gene.g_id in ids:
                    genes.append(gene)
        return genes

    def mutate(self):
        """
        Mutates a chromosome randomly.
        It randomly chooses a gene in the chromosome and a gene that is not yet used
        and switches between them.
        :return:
        """
        num_to_mutate = random.randint(1, len(self.chromosome))
        random.shuffle(self.chromosome)

        # Checking if there are any unused ids. If all ids are used, then a mutation is impossible.
        if self.unused_ids != []:

            # Getting the genes instances which are unused in the chromosome.
            random.shuffle(self.unused_ids)
            unused_genes = self.genes_from_ids(self.unused_ids)

            # There might be more genes in the chromosome than ids that are left and vice versa
            #  so we loop over the min length among the two
            for ind_gene in range(min(num_to_mutate, len(self.unused_ids))):
                self.chromosome[ind_gene] = unused_genes[ind_gene]

            # Update the used ids in the chromosome
            self.chrom_correction()

    def crossover(self, another):
        """
        Gets 2 random chromosomes and does a random crossover between them.
        There are 2 crossover types available - 2 points crossover and 1 point crossover.
        A crossover type is selected randomly.
        :param another:
        :return:
        """
        # One point crossover or two points crossover.
        crossover_type = random.random()

        # Defining the parents and their children
        parent_a = self.chromosome
        parent_b = another.chromosome
        a_ids = list(self.ids)
        b_ids = list(another.ids)

        a_len, b_len = len(parent_a), len(parent_b)
        child_a, child_b = Chromosome(self.items, self.max_weight, self.log), Chromosome(self.items, self.max_weight,
                                                                                         self.log)

        # Two Points Crossover (50% chance to do use this crossover)
        if crossover_type > 0.5:
            num_to_sub = random.randint(1, min(a_len, b_len))
            start_point_l = random.randint(0, a_len - num_to_sub)
            start_point_r = random.randint(0, b_len - num_to_sub)

            # Getting the ids sub sets that are going to be substituted
            sub_genes_a = a_ids[start_point_l:start_point_l + num_to_sub]
            sub_genes_b = b_ids[start_point_r:start_point_r + num_to_sub]

            # Popping out genes that already exist (prevent duplicates)
            for ind, gene_id in enumerate(sub_genes_b):
                if gene_id in a_ids[:start_point_l] + a_ids[start_point_l + num_to_sub:]:
                    sub_genes_b[ind] = -1  # gene's id is not relevant anymore. marked with -1

            for ind, gene_id in enumerate(sub_genes_a):
                if gene_id in b_ids[:start_point_r] + b_ids[start_point_r + num_to_sub:]:
                    sub_genes_a[ind] = -1  # gene's id is not relevant anymore. marked with -1

            child_a.chromosome = parent_a[:start_point_l] + self.genes_from_ids(sub_genes_b, parent_b) + parent_a[
                                                                                                         start_point_l + num_to_sub:]
            child_b.chromosome = parent_b[:start_point_r] + self.genes_from_ids(sub_genes_a, parent_a) + parent_b[

                                                                                                         start_point_r + num_to_sub:]
        # One Point Crossover (50% chance to do use this crossover)
        else:
            point = random.randint(1, min(a_len, b_len))
            # Getting the ids sub sets that are going to be substituted
            sub_genes_a_1 = a_ids[:point]
            sub_genes_a_2 = b_ids[:point]
            sub_genes_b_1 = b_ids[:point]
            sub_genes_b_2 = a_ids[:point]

            # Popping out genes that already exist (prevent duplicates)
            for ind, gene_id in enumerate(sub_genes_a_2):
                if gene_id in sub_genes_a_1:
                    sub_genes_a_2[ind] = -1  # gene's id is not relevant anymore. marked with -1

            for ind, gene_id in enumerate(sub_genes_b_2):
                if gene_id in sub_genes_b_1:
                    sub_genes_b_2[ind] = -1  # gene's id is not relevant anymore. marked with -1

            child_a.chromosome = self.genes_from_ids(sub_genes_a_1, parent_a) + self.genes_from_ids(sub_genes_a_2,
                                                                                                    parent_b)
            child_b.chromosome = self.genes_from_ids(sub_genes_b_1, parent_b) + self.genes_from_ids(sub_genes_b_2,
                                                                                                    parent_a)

        if child_a.chromosome == []:
            child_a.create_random_chromosome()
        if child_b.chromosome == []:
            child_b.create_random_chromosome()

        child_a.chrom_correction()
        child_b.chrom_correction()
        return child_a, child_b
