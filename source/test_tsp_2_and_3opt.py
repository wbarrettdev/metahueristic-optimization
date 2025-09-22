'''
Programme to test various local improvement methods
Example of execution:
Number of cities:
500
Random solution: 24565
Cost of solution found with 2-opt first: 953
Solution improved with 3-opt limited (100 cities): 870
Solution improved with complete 3-opt: 672
Solution improved with 2-opt best: 669
'''
import math

from random_generators import *                                  # Listing %*\ref{lst:random_generators}*)
from tsp_utilities import *                                      # Listing %*\ref{lst:tsp_utilities}*)
from tsp_2opt_first import tsp_2opt_first                        # Listing  %*\ref{lst:tsp_2opt_first}*)
from tsp_2opt_best import tsp_2opt_best                          # Listing  %*\ref{lst:tsp_2opt_best}*)
from tsp_3opt_limited import tsp_3opt_limited                    # Listing  %*\ref{lst:tsp_3opt_limited}*)
from tsp_3opt_first import tsp_3opt_first                        # Listing  %*\ref{lst:tsp_3opt_first}*)

print('Number of cities: ')
n = int(input())

distances = rand_sym_matrix(n, 1, 99)
solution = rand_permutation(n)

length = tsp_length(distances, solution)
print('Random solution: {:d}'.format(length))

solution, length = tsp_2opt_first(distances, solution, length)
print('Cost of solution found with 2-opt first: {:d}'.format(length))

successors = tsp_tour_to_succ(solution)
successors, length = tsp_3opt_limited(distances, 100, successors, length)
print('Solution improved with 3-opt limited (100 cities): {:d}'
      .format(length))

successors, length = tsp_3opt_first(distances, successors, length)
print('Solution improved with complete 3-opt: {:d}'.format(length))

solution = tsp_succ_to_tour(successors)
solution, length = tsp_2opt_best(distances, solution, length)
print('Solution improved with 2-opt best: {:d}'.format(length))
