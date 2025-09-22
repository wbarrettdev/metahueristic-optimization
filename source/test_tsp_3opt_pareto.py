'''
Program to test pareto local seach for the TSP with 3-opt moves
Example of run with K = 3 (KD-tree Key = costs; Info = tour)

Number of cities: 
6
Key:  [137, 253, 273]  Info:  [5, 3, 0, 4, 2, 1]
Key:  [173, 287, 236]  Info:  [2, 4, 5, 0, 3, 1]
Key:  [222, 288, 235]  Info:  [2, 3, 4, 0, 5, 1]
Key:  [263, 249, 242]  Info:  [3, 5, 4, 1, 0, 2]
Key:  [172, 265, 244]  Info:  [4, 5, 0, 1, 3, 2]
Key:  [182, 224, 320]  Info:  [5, 2, 4, 0, 3, 1]
Key:  [184, 244, 297]  Info:  [1, 5, 4, 0, 3, 2]
Key:  [166, 340, 264]  Info:  [1, 3, 0, 4, 5, 2]
Key:  [246, 367, 201]  Info:  [3, 4, 0, 1, 5, 2]
'''
import sys
from random_generators import rand_sym_matrix                    # Listing %*\ref{lst:random_generators}*)
from kd_tree_add_scan import K, kd_tree_scan                     # Listing %*\ref{lst:kd_tree_add_scan}*)
from tsp_3opt_pareto import tsp_3opt_pareto                      # Listing  %*\ref{lst:tsp_3opt_pareto}*)

sys.setrecursionlimit(50000)   # Higly recursive implementation; enlarge stack!
print('Number of cities: ')
n = int(input())

distance = [rand_sym_matrix(n,1,99) for _ in range(K)]
successors = [(i + 1) % n for i in range(n)]                 # Initial solution
costs = [0 for _ in range(K)]
for dim in range(K):
    for i in range(n):
        costs[dim] += distance[dim][i][successors[i]]

pareto = tsp_3opt_pareto(None, costs, successors, distance)

kd_tree_scan(pareto) #Print pareto front with tours (successors representation)
