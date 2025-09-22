######### Pareto local search for the TSP based on 3-opt neighbourhood
def tsp_3opt_pareto(pareto,                                      # Pareto front
                    costs,                   # Tour length (for each dimension)
                    s,                      # Solution (successor of each city)
                    d):              # Distance matrix (one for each dimension)
    from kd_tree_update_pareto import update_3opt_pareto         # Listing %*\ref{lst:kd_tree_update_pareto}*)
    from kd_tree_add_scan import K                               # Listing %*\ref{lst:kd_tree_add_scan}*)
    from random_generators import unif                           # Listing %*\ref{lst:random_generators}*)
    costs_neighbour = [-1 for _ in range(K)]       # Cost of neighbour solution
    start = unif(0, len(s)-1)               # Starting city for move evaluation
    i, j, k = start, s[start], s[s[start]]             # Indices of a 3opt move
    while s[s[i]] != start:            # Neighbourhood not completely evaluated
        for dim in range(K):
            costs_neighbour[dim] = costs[dim] \
               + d[dim][i][s[j]] + d[dim][j][s[k]]  + d[dim][k][s[i]] \
               - d[dim][i][s[i]] - d[dim][j][s[j]]  - d[dim][k][s[k]]
        s[i], s[j], s[k] = s[j], s[k], s[i]      # Change solution to neighbour
        pareto = update_3opt_pareto(pareto, costs_neighbour, s, d)
        s[k], s[j], s[i] = s[j], s[i], s[k]                  # Back to solution
        k = s[k]                                                       # Next k
        if k == i:                                # k at its last value, next j
            j = s[j]; k = s[j]
        if k == i:                                # j at its last value, next i
            i = s[i]; j = s[i]; k = s[j]
    return pareto

