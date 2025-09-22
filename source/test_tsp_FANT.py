'''
Programme to test the Fast Ant procedure
Example of execution

Number of cities:
200
Number of FANT iterations:
200
FANT parameter:
30
FANT 1  314
FANT 2  310
FANT 75  308
FANT 175  306
Cost of solution found with FANT 306
'''

from random_generators import rand_sym_matrix                    # Listing %*\ref{lst:random_generators}*)
from tsp_FANT import tsp_FANT                                    # Listing  %*\ref{lst:tsp_FANT}*) 

print('Number of cities: ')
n = int(input())
print('Number of FANT iterations: ')
fant_iterations = int(input())
print('FANT parameter (best solution reinforcement): ')
fant_parameter = int(input())


distances = rand_sym_matrix(n, 1, 99)
tour, cost = tsp_FANT(distances, fant_parameter, fant_iterations)
print('Cost of solution found with FANT: {:d}'.format(cost))
