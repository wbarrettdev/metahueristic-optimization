from build_2opt_data_structure import build_2opt_data_structure  # Listing  %*\ref{lst:build_2opt_data_structure}*)
from tsp_utilities import tsp_2opt_data_structure_to_tour        # Listing %*\ref{lst:tsp_utilities}*)

######### Local search with 2-opt neighbourhood and first improvement policy
def tsp_2opt_first(d,                                         # Distance matrix
                   tour,                                             # Solution 
                   length):                                   # Solution length

    n = len(tour)
    t = build_2opt_data_structure(tour)
    i = last_i = 0          # i = starting city || last_i = i - a complete tour
    while t[t[i]] != last_i:       # Index i has made 1 turn without impovement
        j = t[t[i]]                                
        while j != last_i and (t[j] != last_i or i != last_i):
            delta =  d[i>>1][j>>1]    + d[t[i]>>1][t[j]>>1] \
                   - d[i>>1][t[i]>>1] - d[j>>1][t[j]>>1]
            if delta < 0:                          # An improving move is found
                next_i, next_j = t[i], t[j]                      # Perform move 
                t[i], t[j] = j ^ 1, i ^ 1               
                t[next_i ^ 1], t[next_j ^ 1] = next_j, next_i

                length += delta                          # Update solution cost
                last_i = i        # Solution improved: i must make another turn
                j = t[i]    
            j = t[j]                                                   # Next j
        i = t[i]                                                       # Next i

    return tsp_2opt_data_structure_to_tour(t), length
