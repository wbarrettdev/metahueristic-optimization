from tsp_utilities import tsp_length                             # Listing %*\ref{lst:tsp_utilities}*)
from tsp_nearest_neighbour import *                              # Listing  %*\ref{lst:tsp_nearest_neighbour}*)

######### Constructive algorithm with Nearest Neighbour as Pilot method
def tsp_pilot_nearest_neighbour(n,                           # Number of cities
                                d):                           # Distance matrix
    tour = [i for i in range(n)]                   # All cities must be in tour

    for q in range(n - 1):             # Cities up to q at their final position
        length_r = tsp_length(d, tour)
        to_insert = q
        for r in range(q, n):        # Choose next city to insert at position q
            sol = [tour[i] for i in range(n)]             # Copy of tour in sol
            sol[q], sol[r] = sol[r], sol[q]       # Tentative city at postion q
            sol[q:n], _ = tsp_nearest_neighbour(d, sol[q:n])
            tentative_length = tsp_length(d, sol)
            if length_r > tentative_length:
                length_r = tentative_length
                to_insert = r       
                        
        # Put definitively to_insert at position q
        tour[q], tour[to_insert] = tour[to_insert], tour[q] 

    return tour, tsp_length(d, tour)
