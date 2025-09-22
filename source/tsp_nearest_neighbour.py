######### Nearest Neighbour greedy heuristic for the TSP
def tsp_nearest_neighbour(d,                                  # Distance matrix
                          tour):                   # List of cities to sequence

    n = len(tour)
    length = 0                                                    # Tour length
    for i in range(1, n):          # Cities from tour[0] to tour[i-1] are fixed
        nearest = i                               # Next nearest city to insert
        cost_ins = d[tour[i-1]][tour[i]]                  # City insertion cost
        for j in range(i+1, n):                      # Find next city to insert
            if d[tour[i-1]][tour[j]] < cost_ins:
                cost_ins = d[tour[i-1]][tour[j]]
                nearest = j
        length += cost_ins
        tour[i], tour[nearest] = tour[nearest], tour[i]  # Definitive insertion

    length += d[tour[n - 1]][tour[0]]                      # Come back to start

    return tour, length
