import os
import numpy as np
from weighted_levenshtein import lev
import heapq
from searchapp.index_and_dict import indexAccess
import re

# for testing
insert_costs = np.ones(128, dtype=np.float64)

# inspired by https://docs.python.org/3/library/heapq.html#heapq.nsmallest
def check_spelling(input, N, model):
    path_to_index = os.path.join(os.getcwd(), 'searchapp','index_and_dict', 'index.json')
    # path_to_index = os.path.join(os.getcwd(), '..','index_and_dict', 'index.json')
    index = indexAccess.getInvertedIndex(path_to_index=path_to_index)

    input_terms = input.split(' ')
    mispelled_term = False
    for term in input_terms:
        if term not in index:
            mispelled_term = True

    if not mispelled_term:
        return []

    print("'" + input + "'" + ' not in index')
    suggestions = []
    for term in input_terms:
        if term not in index:
            h = construct_heap(index, term)
            suggestions.append([heapq.heappop(h)[1] for i in range(N)])
        else:
            suggestions.append([term for i in range(N)])

    formatted_suggestions = format_suggestions(suggestions, len(input_terms), N)
    return formatted_suggestions

def format_suggestions(suggestions, rows, cols):
    formatted_sugestions = []
    for j in range(cols):
        suggestion = ''
        for i in range(rows):
            suggestion += suggestions[i][j] + ' '
        formatted_sugestions.append(suggestion)
    return formatted_sugestions

# inspired by https://docs.python.org/3/library/heapq.html#heapq.nsmallest
def construct_heap(index, input):
    h = []
    for value in index:
        try:
            pattern = re.compile('[\W_]*[0-9]*', re.UNICODE) # inspired by https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python
            value = pattern.sub('', value)
            dist = lev(input, value, insert_costs)
        except:
            continue
        heapq.heappush(h, (dist, value))
    return h