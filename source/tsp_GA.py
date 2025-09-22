from random_generators import rand_permutation                   # Listing %*\ref{lst:random_generators}*)
from tsp_utilities import tsp_length                             # Listing %*\ref{lst:tsp_utilities}*)
from rank_based_selection import *                               # Listing %*\ref{lst:rank_based_selection}*)
from OX_crossover import OX_crossover                            # Listing %*\ref{lst:OX_crossover}*)
from mutate import mutate                                        # Listing %*\ref{lst:mutate}*)
from insert_child import insert_child                            # Listing %*\ref{lst:insert_child}*)
from tsp_LK import tsp_LK                                        # Listing %*\ref{lst:tsp_LK}*)

######### Basic Memetic Algorithm for the TSP
def tsp_GA(d,                           # Distance matrix (must be symmetrical)
           population_size,                            # Size of the population
           generations,                                 # Number of generations
           mutation_rate): 

    n = len(d[0])
    population = [rand_permutation(n) for _ in range(population_size)]
    lengths = [tsp_length(d, population[i]) for i in range(population_size)]

    order = [i for i in range(population_size)]
    for i in range(population_size - 1):
        for j in range(i + 1, population_size):
            if lengths[order[i]] > lengths[order[j]]:
                order[i], order[j] = order[j], order[i]
    print('GA initial best individual {:d}'.format(lengths[order[0]]))

    for gen in range(generations):
        parent1 = rank_based_selection(population_size)
        parent2 = rank_based_selection(population_size)
        child = OX_crossover(population[order[parent1]], 
                             population[order[parent2]])
        child = mutate(mutation_rate, child)
        child_length = tsp_length(d, child)
        child, child_length = tsp_LK(d, child, child_length)
        child_rank, population, lengths, order = insert_child(child,
                     child_length, population_size, population, lengths, order)
        if child_rank == 0:
           print('GA improved tour {:d} {:d}'.format(gen, child_length))
    return population[order[0]], lengths[order[0]]
