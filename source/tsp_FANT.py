from random_generators import rand_permutation                   # Listing %*\ref{lst:random_generators}*)
from generate_solution_trail import *                            # Listing  %*\ref{lst:generate_solution_trail}*)
from init_update_trail import *                                  # Listing  %*\ref{lst:init_update_trail}*)
from tsp_LK import tsp_LK                                        # Listing %*\ref{lst:tsp_LK}*)

######### Fast Ant System for the TSP
def tsp_FANT(d,                                               # Distance matrix
             exploitation,              # FANT Parameters: global reinforcement
             iterations):                      # number of solution to generate

    n = len(d[0])
    best_cost = float('inf')
    exploration = 1
    trail = [[-1] * n for _ in range(n)]
    trail = init_trail(exploration, trail)
    tour = rand_permutation(n)
    for i in range(iterations):
        # Build solution
        tour, cost = generate_solution_trail(d, tour, trail)
        # Improve built solution with a local search
        tour, cost = tsp_LK(d, tour, cost)
        if cost < best_cost:
            best_cost = cost
            print('FANT {:d} {:d}'.format(i+1, cost))
            best_sol = list(tour)
            exploration = 1                 # Reset exploration to lowest value
            trail = init_trail(exploration, trail)
        else:
            # Pheromone trace reinforcement - increase memory
            trail, exploration = update_trail(tour, best_sol,
                                              exploration, exploitation, trail)
    return best_sol, best_cost
