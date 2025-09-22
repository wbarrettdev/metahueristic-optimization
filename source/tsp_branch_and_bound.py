from tsp_lower_bound import tsp_lower_bound                       # Listing %*\ref{lst:tsp_lower_bound}*)

######### Basic Branch & Bound for the TSP 
def tsp_branch_and_bound(d,                                   # Distance matrix
                         depth,  # current_tour[0] to current_tour[depth] fixed
                         current_tour,               # Solution partially fixed
                         best_tour,                       # Best solution found
                         upper_bound):                    # Optimum tour length

    n = len(current_tour)
    for i in range(depth, n):
        tour = current_tour[:]
        tour[depth], tour[i] = tour[i], tour[depth] # City enumeration at depth
        lb, tour, valid = tsp_lower_bound(d, depth, tour)
        if (upper_bound > lb):
            if (valid):
                upper_bound = lb
                best_tour = tour[:]
                print("Improved: ", upper_bound, best_tour)
            else:
              best_tour, upper_bound =  \
                 tsp_branch_and_bound(d, depth+1, tour, best_tour, upper_bound)
    return best_tour, upper_bound    
