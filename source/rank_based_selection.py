import math
from random_generators import unif                               # Listing %*\ref{lst:random_generators}*)

######### Selection operator for reproduction based on the rank
def rank_based_selection(size):
    return int(size \
               - math.ceil(math.sqrt(.25 + 2*unif(1, size*(size + 1)/2)) - .5))
