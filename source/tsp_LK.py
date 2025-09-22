from tsp_utilities import *                                      # Listing %*\ref{lst:tsp_utilities}*)

######### Basic Lin & Kernighan improvement procedure for the TSP
def tsp_LK(D,                                                 # Distance matrix
           tour,                                                     # Solution 
           length):                                               # Tour length
    n = len(tour)
    succ = tsp_tour_to_succ(tour)
    for i in range(n): succ[tour[i]] = tour[(i + 1) % n]
    tabu = [[0 for _ in range(n)] for _ in range(n)] #Can edge i-j be removed ?
    iteration = 0           # Outermost loop counter to identify tabu condition
    last_a, a = 0, 0                  # Initiate ejection chain from city a = 0
    improved = True
    while a != last_a or improved:
        improved = False
        iteration += 1
        b = succ[a]
        path_length = length - D[a][b]
        path_modified = True
        while path_modified: # Identify best ref. struct. with edge a-b removed
            path_modified = False
            ref_struct_cost = length     # Cost of reference structure retained
            c = best_c = succ[b]
            while succ[c] != a:                    # Ejection can be propagated
                d = succ[c]
                if path_length - D[c][d] + D[c][a] + D[b][d] < length:
                    best_c = c            # An improving solution is identified
                    ref_struct_cost = path_length - D[c][d] + D[c][a] + D[b][d]
                    break               # Change improving solution immediately
                if tabu[c][d] != iteration and \
                                 path_length + D[b][d] < ref_struct_cost:
                    ref_struct_cost = path_length + D[b][d]
                    best_c = c
                c = d                                  # Next value for c and d
            if ref_struct_cost < length: # Admissible reference structure found
                path_modified = True
                c, d = best_c, succ[best_c]        # Update reference structure
                tabu[c][d] = tabu[d][c] = iteration#Don't remove again edge c-d
                path_length += (D[b][d] - D[c][d])
                i, si, succ[b] = b, succ[b], d            # Reverse path b -> c
                while i != c:
                    succ[si], i, si = i, si, succ[si]
                b = c
                
                if path_length + D[a][b] < length: # A better solution is found
                    length = path_length + D[a][b]  
                    succ[a], last_a = b, b
                    improved = True
                    tour = tsp_succ_to_tour(succ)
        succ = tsp_tour_to_succ(tour)
        a = succ[a]
    return tour, length
