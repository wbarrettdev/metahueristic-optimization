'''
Programme to test a basic memetic algorithm
Example of execution:
Number of cities: 
200
Size of the population: 
10
Mutation rate: 
0.02
Number of generations: 
30
GA initial best individual 9424
GA improved tour 0 313
GA improved tour 7 312
GA improved tour 15 307
Cost of solution found with GA: 307

'''


from random_generators import rand_sym_matrix                    # Listing %*\ref{lst:random_generators}*)
from tsp_GA import tsp_GA                                        # Listing %*\ref{lst:tsp_GA}*)

print('Number of cities: ')
n = int(input())
print('Size of the population: ')
population_size = int(input())
print('Mutation rate: ')
mutation_rate = float(input())
print('Number of generations: ')
nr_generations = int(input())

distances = rand_sym_matrix(n, 1, 99)
_, cost = tsp_GA(distances, population_size, nr_generations, mutation_rate)
print('Cost of solution found with GA: {:d}'.format(cost))
