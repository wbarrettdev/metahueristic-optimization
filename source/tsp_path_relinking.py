from tsp_utilities import tsp_succ_to_pred                       # Listing %*\ref{lst:tsp_utilities}*)

######### Path relinking for the TSP, based on 3-opt neighbourhood
def tsp_path_relinking(d,                                     # Distance matrix
                       target,                   # Target solution (successors)
                       length,                     # Length of current solution
                       succ):                               # Starting solution

    best_succ = succ[:]
    best_length = length
    pred = tsp_succ_to_pred(succ)
    best_delta = -1
    while best_delta < float('inf'):
        best_delta = float('inf')
        i = best_i = best_j = best_k = pred[0]
        while best_delta >= 0 and i != 0:
            i = succ[i]
            if succ[i] != target[i]:
                j = pred[target[i]]
                k = target[i]
                while k != i:
                    if succ[k] != target[k]:
                        delta = d[i][succ[j]] + d[j][succ[k]] + d[k][succ[i]] \
                               -d[i][succ[i]] - d[j][succ[j]] - d[k][succ[k]]
                        if delta < best_delta:
                            delta = best_delta
                            best_i, best_j, best_k = i, j, k
                    k = succ[k]
        if best_delta < float('inf'):
            i, j, k = best_i, best_j, best_k
            length += best_delta;
            pred[succ[i]], pred[succ[j]], pred[succ[k]] = k, i, j;
            succ[j], succ[k], succ[i] = succ[k], succ[i], target[i];
            if length < best_length:
                best_length = length
                best_succ = succ[:]
    return best_succ, best_length
