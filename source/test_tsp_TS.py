'''
Program to test a Taboo Search for the TSP
Example of run:
Number of cities: 
30
Number of tabu iterations: 
200
Minimum tabu_duration: 
4
Maximum tabu_duration: 
20
Penalty: 
0.005
TS 1 1190
TS 2 1053
TS 3 906
TS 4 796
...
TS 29 177
TS 46 174
TS 119 173
Cost of solution found : 173
[13, 0, 6, 5, 27, 28, 1, 4, 29, 20, 2, 7, 16, ...24, 9, 21, 25, 10, 22, 19, 14]
'''
import math

from random_generators import *                                  # Listing %*\ref{lst:random_generators}*)
from tsp_utilities import tsp_length                             # Listing %*\ref{lst:tsp_utilities}*)
from tsp_TS import tsp_TS                                        # Listing  %*\ref{lst:tsp_TS}*)

print('Number of cities: ')
n = int(input())

distances = rand_sym_matrix(n, 1, 99)
solution = rand_permutation(n)
length = tsp_length(distances, solution)


print('Number of tabu iterations: ')
iterations = int(input())
print('Minimum tabu_duration: ')
min_tabu = int(input())
print('Maximum tabu_duration: ')
max_tabu = int(input())
print('Penalty: ')
freq_penalty = float(input())
solution, length = tsp_TS(distances, solution, length, 
                          iterations, min_tabu, max_tabu, freq_penalty)
print('Cost of solution found : {:d}'.format(length))
print(solution)
