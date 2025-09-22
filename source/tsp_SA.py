import math
from random_generators import unif, rando                        # Listing %*\ref{lst:random_generators}*)

######### Basic Simulated Annealing for the TSP, based on 2-opt moves
def tsp_SA(d,                                                 # Distance matrix
           tour,                                                     # TSP tour
           length,                                                # Tour length
           initial_temperature,                                 # SA parameters
           final_temperature, 
           alpha):

    n = len(tour)
    best_length = length
    best_tour = tour
    T = initial_temperature
    iteration = 0
    while T > final_temperature:
        i = unif(0, n-1)                 # First city of a move randomly chosen
        j = (i + unif(2, n-2))%n       # Second city is unif successors further
        if j < i:
          i, j = j, i                           # j must be further on the tour
        delta =  d[tour[i]][tour[j]]     + d[tour[i+1]][tour[(j+1) % n]]\
                -d[tour[i]][tour[i + 1]] - d[tour[j]][tour[(j + 1) % n]]
        if delta < 0 or math.exp(-delta / T) > rando():
            length = length + delta                             # Move accepted
            for k in range((j - i) // 2):    # Reverse sub-path between i and j
                tour[k + i + 1], tour[j - k] = tour[j - k], tour[k + i + 1]

        # is there an improvement?
        if best_length > length:
            best_length = length
            best_tour = tour
            print('SA {:d} {:d}'.format(iteration, length))
        iteration += 1
        if iteration % (n * n) == 0:
            T *= alpha                                   # Decrease temperature
    return best_tour, best_length
