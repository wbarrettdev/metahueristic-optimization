from random_generators import rand_permutation                   # Listing %*\ref{lst:random_generators}*)
from tsp_utilities import tsp_length                             # Listing %*\ref{lst:tsp_utilities}*)
from tsp_LK import tsp_LK                                        # Listing %*\ref{lst:tsp_LK}*)

######### Procedure for producing a TSP tour using GRASP principles
def tsp_GRASP(d,                                              # Distance matrix
              alpha):

    n = len(d[0])
    tour = rand_permutation(n)
    for i in range(n - 1):
        # determine c_min and c_max incremental costs
        c_min, c_max = float('inf'), float('-inf')
        for j in range(i + 1, n):
            if c_min > d[tour[i]][tour[j]]:
                c_min = d[tour[i]][tour[j]]
            if c_max < d[tour[i]][tour[j]]:
                c_max = d[tour[i]][tour[j]]
            
        next = i+1          # Find the next city to insert, based on lower cost
        while d[tour[i]][tour[next]] > c_min + alpha * (c_max - c_min):
            next += 1
        tour[i + 1], tour[next] = tour[next], tour[i + 1]

    length = tsp_length(d, tour)
    tour, length = tsp_LK(d, tour, length)
    return tour, length
