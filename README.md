# Genetic-Algorithm-Knapsack-problem
Evolutionary algorithm heuristic approach for the standard 0-1 Knapsack problem.
This algorithm assumes each item has value and weight. Our target is to maximize the total value given the weight constraint, or in other words:

![problem_definition](https://github.com/ShaikeA/Genetic-Algorithm-Knapsack-problem/blob/master/problem_def.JPG)

## Usage

Under the data folder, fill into ```items.txt``` the items' weights in the following format:
``` 
[Value Weight]
```

 For example:
```
6 2
5 3
8 6
9 7
6 5
7 9
3 4
2 3
4 6
8 8
2 2
4 3
10 5
8 9
10 2
4 1
5 2
3 3
4 2
6 8
```

Then, cd to your the main directory and type: 
```bash
python main.py
```
You will be asked to specify the max weight of the Knapsack. Type an integer and hit enter.



## Outputs
There will be 2 outputs: 

1. A graph showing the progress over the iterations (generations)

![fitness_over_generations](https://github.com/ShaikeA/Genetic-Algorithm-Knapsack-problem/blob/master/fitness_over_gen.png)

2. The algorithm's results every 100 iterations and the best found chromosomes:
It consists of a list of all genes where each gene is represented by (id, value, weight).

Generation 0:
Max score 66.0 | Chromosome: [(12, 10.0, 5.0), (6, 3.0, 4.0), (11, 4.0, 3.0), (3, 9.0, 7.0), (18, 4.0, 2.0), (9, 8.0, 8.0), (10, 2.0, 2.0), (15, 4.0, 1.0), (14, 10.0, 2.0), (16, 5.0, 2.0), (7, 2.0, 3.0), (1, 5.0, 3.0)]

Generation 100:
Max score 71.0 | Chromosome: [(12, 10.0, 5.0), (2, 8.0, 6.0), (11, 4.0, 3.0), (3, 9.0, 7.0), (18, 4.0, 2.0), (9, 8.0, 8.0), (10, 2.0, 2.0), (15, 4.0, 1.0), (14, 10.0, 2.0), (16, 5.0, 2.0), (7, 2.0, 3.0), (1, 5.0, 3.0)]

Best chromosomes: [[(12, 10.0, 5.0), (2, 8.0, 6.0), (11, 4.0, 3.0), (3, 9.0, 7.0), (0, 6.0, 2.0), (9, 8.0, 8.0), (10, 2.0, 2.0), (15, 4.0, 1.0), (14, 10.0, 2.0), (16, 5.0, 2.0), (7, 2.0, 3.0), (1, 5.0, 3.0)], [(12, 10.0, 5.0), (2, 8.0, 6.0), (11, 4.0, 3.0), (3, 9.0, 7.0), (18, 4.0, 2.0), (9, 8.0, 8.0), (10, 2.0, 2.0), (15, 4.0, 1.0), (14, 10.0, 2.0), (16, 5.0, 2.0), (7, 2.0, 3.0), (0, 6.0, 2.0)]]


