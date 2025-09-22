######### Computation of a naive lower bound for the TSP
def tsp_lower_bound(d,                                        # Distance matrix
                    depth,                       # tour[0] to tour[depth] fixed
                    tour):                                           # TSP tour

    n = len(tour)
    lb = 0 #Compute the length of the path for the cities already fixed in tour
    for j in range(depth):
      lb += d[tour[j]][tour[j+1]]

    valid = 1  # valid is set to 1 if every closest successor of j build a tour
    for j in range(depth, n-1):     # Add the length to the closest free city j
        minimum = d[tour[j]][tour[j+1]]
        for k in range(n-1, depth, -1):
            if k != j and minimum > d[tour[j]][tour[k]]:
                minimum = d[tour[j]][tour[k]]
                if (k > j):
                    tour[k], tour[j+1] = tour[j+1], tour[k]
                else:
                    valid = 0
        lb += minimum

    minimum = d[tour[n-1]][tour[0]]       # Come back to first city of the tour
    for j in range (depth+1, n-1):
        if (minimum > d[tour[j]][tour[0]]):
            valid = 0
            minimum = d[tour[j]][tour[0]]
    lb += minimum
    return lb, tour, valid      # Lower bound, tour modified, lb == tour length
