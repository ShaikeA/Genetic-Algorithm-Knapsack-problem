"""
Main knapsack script.
This scripts uses Genetic Algorithm in order to solve the knapsack problem.
Given a list of items with values and weights, we want to maximize the total value
of the knapsack given the constraint of max weight.
"""

import numpy as np
from collections import defaultdict
from ga_components.Population import Population
from logs.Logger import Logger
import click
from ga_tests.tests import Tests
import os

POP_SIZE = 20
cur_path = os.getcwd()
txt_file = os.path.join(cur_path, 'data', 'items.txt')
items = np.loadtxt(txt_file)
len_items = items.shape[0]
ids = np.arange(len_items).reshape(len_items, -1)
ITEMS = defaultdict(list, {ind: list(items[ind]) for ind in range(len(items))})


@click.command()
@click.option('--weight', '-w', default=1, type=int, prompt='Specify the max weight of the Knapsack',
              help='Enter a positive integer as the max weight of the knapsack.')
def main(weight):

    # Defining logger class
    log = Logger()

    # Creating and running tests
    test = Tests()
    test.run_all_tests()

    # Creating an initial population and running the evolution method
    pop = Population(ITEMS, weight, POP_SIZE, log)
    log.logger.info("Population has been created")
    pop.create_initial_pop()
    pop.evolution(select_elite=int(.1 * POP_SIZE))


if __name__ == '__main__':
    main()
