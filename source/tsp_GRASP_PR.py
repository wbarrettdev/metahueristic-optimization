from random_generators import unif                               # Listing %*\ref{lst:random_generators}*)
from tsp_utilities import *                                      # Listing %*\ref{lst:tsp_utilities}*)
from tsp_GRASP import tsp_GRASP                                  # Listing  %*\ref{lst:tsp_GRASP}*)
from tsp_path_relinking import tsp_path_relinking                # Listing %*\ref{lst:tsp_path_relinking}*)

######### GRASP with path relinking for the TSP
def tsp_GRASP_PR(d,                                           # Distance matrix
                 iterations,                         # Number of calls to GRASP
                 population_size,                      # Size of the population
                 alpha):                                      # GRASP parameter

    n = len(d[0])
    population = [[-1] * population_size for _ in range(population_size)]
    pop_size = iteration = 0
    lengths = [-1] * population_size
    while (pop_size < population_size and iteration < iterations):
        tour, tour_length = tsp_GRASP(d, alpha)
        iteration += 1
        succ = tsp_tour_to_succ(tour)
        different = True
        for i in range(pop_size - 1):
            if tsp_compare(population[i], succ) == 0:
                different = False
                break                       # The tour is already in population
        if different:
            population[pop_size] = succ[:]
            lengths[pop_size] = tour_length
            pop_size += 1
    if (iteration == iterations):#Unable to generate enough different solutions
        population_size = pop_size
    for it in range(iteration, iterations):
        tour, tour_length = tsp_GRASP(d, alpha)
        iteration += 1
        succ = tsp_tour_to_succ(tour)
        successors, length = tsp_path_relinking(d, 
                       population[unif(0,population_size-1)],tour_length, succ)
        max_difference, replacing = -1, -1
        for i in range(population_size):
            if (length <= lengths[i]):
                difference = tsp_compare(population[i], successors)
                if difference == 0:
                    max_difference = 0
                    break
                if difference > max_difference and length < lengths[i]:
                    max_difference = difference
                    replacing = i
        if max_difference > 0:
            lengths[replacing] = length
            population[replacing] = successors[:]
            print('GRASP_PR population updated:', it, length)

    best = 0
    for i in range(1, population_size):
        if lengths[i] < lengths[best]:
            best = i
    return tsp_succ_to_tour(population[best]), lengths[best]

