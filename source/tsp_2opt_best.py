######### Local search with 2-opt neighbourhood and best improvement policy
def tsp_2opt_best(d,                                          # Distance matrix
                  tour,                                              # Solution 
                  length):                                    # Solution length
    n = len(tour)
    best_delta = -1
    while best_delta < 0:
        best_delta = float('inf')
        best_i = best_j = -1                             # Best move to perform
        for i in range(n - 2):             
            j = i + 2                                       
            while j < n and (i > 0 or j < n - 1):
                delta = \
                    d[tour[i]][tour[j]]   + d[tour[i+1]][tour[(j+1)%n]] \
                  - d[tour[i]][tour[i+1]] - d[tour[j]][tour[(j+1)%n]]
                if delta < best_delta:
                    best_delta = delta
                    best_i, best_j = i, j
                j += 1                                         # Next neighbour

        if best_delta < 0:     # Perform best move if it improves best solution
            length += best_delta                         # Update solution cost
            i, j = best_i+1, best_j      # Reverse path from best_i+1 to best_j
            while i < j:
               tour[i], tour[j] = tour[j], tour[i]
               i, j = i + 1, j - 1

    return tour, length
