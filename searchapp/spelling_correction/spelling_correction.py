import os
import numpy as np
from weighted_levenshtein import lev
import heapq
from searchapp.index_and_dict import indexAccess
import json

# for testing
insert_costs = np.ones(128, dtype=np.float64)

# inspired by https://docs.python.org/3/library/heapq.html#heapq.nsmallest
def check_spelling(input, N):
    path_to_index = os.path.join(os.getcwd(), 'searchapp','index_and_dict', 'index.json')
    index = indexAccess.getInvertedIndex(path_to_index=path_to_index)
    h = construct_heap(index, input);
    return [heapq.heappop(h)[1] for i in range(N)]

# inspired by https://docs.python.org/3/library/heapq.html#heapq.nsmallest
def construct_heap(index, input):
    h = []
    for value in index:
        dist = lev(input, value, insert_costs)
        heapq.heappush(h, (dist, value))
    return h