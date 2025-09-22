from random_generators import unif                               # Listing %*\ref{lst:random_generators}*)
from tsp_utilities import tsp_length                             # Listing %*\ref{lst:tsp_utilities}*)
from tsp_LK import tsp_LK                                        # Listing %*\ref{lst:tsp_LK}*)

######### Record to record iterative local search for the TSP
def tsp_record_to_record(d,              # Distance matrix, must be symmetrical
                         best_tour,                                  # TSP tour
                         best_length,
                         iterations):                    # Number of iterations
    n = len(d[0])
    for iteration in range(1, iterations+1):
        tour = best_tour[:]          # No tolerance: always revert to best tour
        
        for _ in range(2):                                # Perturbate solution
            u = unif(0, n - 1)
            v = unif(0, n - 1)
            tour[u], tour[v] = tour[v], tour[u]
        length = tsp_length(d, tour)
        tour, length = tsp_LK(d, tour, length)
        iteration += 1
        if length < best_length:                     # Store improved best tour
            best_tour = tour[:]
            best_length = length
            print('Record to record {:d}\t {:d}'
                  .format(iteration, length))
    return best_tour, best_length
