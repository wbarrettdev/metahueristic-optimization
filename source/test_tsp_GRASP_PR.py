'''
Program to test a GRASP with Path Relinking
Example of execution:
Number of cities: 
200
Iterations: 
50
Population size: 
10
Alpha: 
0.7
GRASP_PR population updated: 11 319
GRASP_PR population updated: 12 317
GRASP_PR population updated: 13 318
GRASP_PR population updated: 15 318
GRASP_PR population updated: 16 320
GRASP_PR population updated: 18 317
GRASP_PR population updated: 19 315
GRASP_PR population updated: 20 316
GRASP_PR population updated: 21 309
GRASP_PR population updated: 25 316
GRASP_PR population updated: 26 313
GRASP_PR population updated: 35 316
GRASP_PR population updated: 36 313
GRASP_PR population updated: 40 313
GRASP_PR population updated: 42 311
GRASP_PR population updated: 49 313
Cost of solution found with GRASP_PR: 309
'''
from random_generators import rand_sym_matrix                    # Listing %*\ref{lst:random_generators}*)
from tsp_GRASP_PR import tsp_GRASP_PR                            # Listing %*\ref{lst:tsp_GRASP_PR}*)

print('Number of cities: ')
n = int(input())
print('Iterations: ')
iterations = int(input())
print('Population size: ')
population_size = int(input())
print('Alpha: ')
alpha = float(input())

distances = rand_sym_matrix(n, 1, 99)

tour, length = tsp_GRASP_PR(distances, iterations, population_size, alpha)
print('Cost of solution found with GRASP_PR: {:d}'.format(length))
