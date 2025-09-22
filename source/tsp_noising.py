from build_2opt_data_structure import *                          # Listing  %*\ref{lst:build_2opt_data_structure}*)
from random_generators import unif, rando                        # Listing %*\ref{lst:random_generators}*)
from tsp_utilities import *                                      # Listing %*\ref{lst:tsp_utilities}*)
from math import *

######### Noising method for the TSP
def tsp_noising(d,                                            # Distance matrix
                tour,                                                # TSP tour
                length,                                           # Tour length
                initial_noise,                                     # Parameters
                final_noise, 
                alpha):

    n = len(tour)
    t = build_2opt_data_structure(tour)
    current_noise = initial_noise
    best_length = length
    iteration = 0
    while current_noise > final_noise:
        i = unif(0, n-1)                 # First city of a move randomly chosen
        last_i = i
        while t[t[i]]>>1 != last_i and t[i]>>1 != last_i:
            j = t[t[i]]                            
            while j>>1 != last_i and (t[j]>>1 != last_i or i>>1 != last_i):
                delta = d[i >> 1][j >> 1]    + d[t[i] >> 1][t[j] >> 1] \
                       -d[i >> 1][t[i] >> 1] - d[j >> 1][t[j] >> 1]                
                if delta + current_noise * log(rando()) < 0:     # SA criterion
                    length = length + delta                     # Move accepted
                    best_i, best_j = t[i], t[j]
                    t[i], t[j] = j ^ 1, i ^ 1 # New successors and predecessors
                    t[best_i ^ 1], t[best_j ^ 1] = best_j, best_i

                    i = t[i]     # Avoid reversing immediately a degrading move
                    j = t[i]

                    # is there an improvement?
                    if best_length > length:
                        best_length = length
                        tour = tsp_2opt_data_structure_to_tour(t)
                        print('Noising {:d} {:d}'.format(iteration, length))
                iteration += 1
                if iteration % (n * n) == 0:
                    current_noise *= alpha                     # Decrease noise
                j = t[j]                                               # Next j
            i = t[i]                                                   # Next i
    return tour, best_length
