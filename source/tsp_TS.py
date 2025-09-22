from random_generators import *                                  # Listing %*\ref{lst:random_generators}*)

######### Taboo Search for the TSP, based on 2-opt moves
def tsp_TS(d,                                                 # Distance matrix
           tour,                                        # Intital tour provided
           length,                                     # Length of initial tour
           iterations,                       # Number of tabu search iterations
           min_tabu_duration,                           # Minimal tabu duration
           max_tabu_duration,                                  
           F):               # Factor for penalizing moves repeatedly performed
   
    n = len(tour)
    tabu = [[0] * n for _ in range(n)]                              # Tabu list
    count = [[0] * n for _ in range(n)]                            # Move count
    best_tour = tour[:]
    best_length = length
    for iteration in range(0, iterations):
        delta_penalty = float('inf')
        ir = jr = -1                    # Cities retained for performing a move
        # Find best move allowed or aspired
        for i in range(n - 2):
            j = i + 2
            while j < n and (i > 0 or j < n - 1):       
                delta =  d[tour[i]][tour[j]]  + d[tour[i+1]][tour[(j+1) % n]]\
                    -d[tour[i]][tour[i + 1]]  - d[tour[j]][tour[(j + 1) % n]]
                penality =  F * (count[tour[i]][tour[j]]
                                 + count[tour[i + 1]][tour[(j + 1) % n]])
                # Conditions for accepting a candidate move
                better = delta + penality < delta_penalty
                allowed = tabu[tour[i]][tour[j]] <= iteration \
                          or  tabu[tour[i + 1]][tour[(j + 1) % n]] <= iteration
                aspirated = length + delta < best_length

                if better and (allowed or aspirated):
                    delta_penalty = delta + penality
                    ir, jr = i, j
                j += 1                                         # Next neighbour

        # Perform retained move
        if delta_penalty < float('inf'): 
            tabu[tour[ir]][tour[ir + 1]] = tabu[tour[jr]][tour[(jr + 1) % n]] \
            = tabu[tour[ir + 1]][tour[ir]] = tabu[tour[(jr+1) % n]][tour[jr]] \
            = unif(min_tabu_duration, max_tabu_duration) + iteration

            count[tour[ir]][tour[ir + 1]] += 1
            count[tour[jr]][tour[(jr + 1) % n]] += 1
            count[tour[ir + 1]][tour[ir]] += 1
            count[tour[(jr + 1) % n]][tour[jr]] += 1

            length += d[tour[ir]][tour[jr]] + d[tour[ir+1]][tour[(jr+1) % n]]\
                     -d[tour[ir]][tour[ir+1]] - d[tour[jr]][tour[(jr+1) % n]]

            for k in range((jr - ir) // 2):
                tour[k + ir + 1], tour[jr - k] = tour[jr - k], tour[k + ir + 1]
        else:
            print('All moves are forbidden tabu list too long')
        if best_length > length:                     # is there an improvement?
            best_length = length
            best_tour = tour[:]
            print('TS {:d} {:d}'.format(iteration+1, best_length))
    return best_tour, best_length
