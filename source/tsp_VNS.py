from random_generators import unif                               # Listing %*\ref{lst:random_generators}*)
from tsp_utilities import tsp_length                             # Listing %*\ref{lst:tsp_utilities}*)
from tsp_LK import tsp_LK                                        # Listing %*\ref{lst:tsp_LK}*)

######### Variable Neighbourhood Search for the TSP
def tsp_VNS(d,                                                # Distance matrix
            best_tour,                                               # TSP tour
            best_length):            
    n = len(best_tour)
    iteration, k = 1, 1
    while k < n:
        tour = best_tour[:]      
        for _ in range(k):                                # Perturbate solution
            u = unif(0, n - 1)
            v = unif(0, n - 1)
            tour[u], tour[v] = tour[v], tour[u]
        length = tsp_length(d, tour)
        tour, length = tsp_LK(d, tour, length)
        iteration += 1
        if length < best_length:                     # Store improved best tour
            best_tour = tour[:]
            best_length = length
            print('VNS {:d}\t {:d}\t {:d}'
                  .format(iteration, k, length))
            k = 1
        else:
            k += 1                                       # Neighbourhood change
    return best_tour, best_length
