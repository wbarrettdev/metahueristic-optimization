######### POPMUSIC for the TSP based on 3-opt neighbourhood
def tsp_3opt_limited(d,                                       # Distance matrix
                     r,                                       # Subproblem size
                     succ,                         # Tour provided and returned 
                     length):                                     # Tour length
    n = len(succ)
    if r > n:                               # Subproblem size must not exceed n
        r = n
    i = last_i = 0                                   # starting city is index 0
    while True:
        j = succ[i]
        edges_ij, edges_jk = 1, 1 # Number of edges from i to j and from j to k
        while edges_ij + edges_jk < r:
            k = succ[j]
            while edges_ij + edges_jk < r:
                delta = d[i][succ[j]] + d[j][succ[k]] + d[k][succ[i]] \
                       -d[i][succ[i]] - d[j][succ[j]] - d[k][succ[k]]
                if delta < 0:                        # Is there an improvement?
                    length += delta                              # Perform move
                    succ[i], succ[j], succ[k] = succ[j], succ[k], succ[i] 
                    j, k = k, j                     # Replace j between i and k
                    edges_ij, edges_jk = edges_jk, edges_ij
                    last_i = i
                edges_jk += 1
                k = succ[k]                                            # Next k
            edges_jk = 1
            edges_ij += 1
            j = succ[j]                                                # Next j
        i = succ[i]                                                    # Next i
        
        if i == last_i:           # A complete tour scanned without improvement
            break

    return succ, length
