######### Local search with 3-opt neighbourhood and first improvement policy
def tsp_3opt_first(d,                                         # Distance matrix
                   succ,                                             # Solution 
                   length):                                   # Solution length

    last_i, last_j, last_k = 0, succ[0], succ[succ[0]]
    i, j, k = last_i, last_j, last_k
    while True:
        delta = d[i][succ[j]] + d[j][succ[k]] + d[k][succ[i]] \
               -d[i][succ[i]] - d[j][succ[j]] - d[k][succ[k]]       # Move cost
        if delta < 0:                                # is there an improvement?
            length += delta                              # Update solution cost
            succ[i], succ[j], succ[k] = succ[j], succ[k], succ[i]# Perform move
            j, k = k, j                             # Replace j between i and k
            last_i, last_j, last_k = i, j, k
        k = succ[k]                                                    # Next k
        if k == i:                                # k at its last value, next j
            j = succ[j]; k = succ[j]
        if k == i:                                # j at its last value, next i
            i = succ[i]; j = succ[i]; k = succ[j]
        if i == last_i and j == last_j and k == last_k:
          break

    return succ, length
