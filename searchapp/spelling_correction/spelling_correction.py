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
    print(model)
    input = input.lstrip().rstrip()
    input_terms = input.split(' ')
    if model == 'bool':
        return check_spelling_bool(input_terms, N)

    path_to_index = os.path.join(os.getcwd(), 'searchapp','index_and_dict', 'index.json')
    index = indexAccess.getInvertedIndex(path_to_index=path_to_index)

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

def check_spelling_bool(input_terms, N):
    path_to_index = os.path.join(os.getcwd(), 'searchapp','index_and_dict', 'index.json')
    index = indexAccess.getInvertedIndex(path_to_index=path_to_index)

    mispelled_term = False
    for i in range(len(input_terms)):
        term = input_terms[i].replace('(', '').replace(')','')
        if term == 'AND' or term == 'OR' or term == 'AND_NOT':
            continue
        elif term not in index:
            mispelled_term = True

    if not mispelled_term:
        return []

    suggestions = []
    for term in input_terms:
        if term == 'AND' or term == 'OR' or term == 'AND_NOT':
            suggestions.append([term for i in range(N)])
        elif term not in index:
            front_par_count = term.count('(')
            back_par_count = term.count(')')
            term = term.replace('(', '')
            term = term.replace(')', '')

            h = construct_heap(index, term)
            n_suggestions = [heapq.heappop(h)[1] for i in range(N)]
            if front_par_count > 0:
                for x in range(len(n_suggestions)):
                    word_par = ''
                    for i in range(front_par_count):
                        word_par += '('
                    word_par += n_suggestions[x]
                    n_suggestions[x] = word_par
            elif back_par_count > 0:
                for x in range(len(n_suggestions)):
                    word_par = n_suggestions[x]
                    for i in range(back_par_count):
                        word_par += ')'
                    n_suggestions[x] = word_par

            suggestions.append(n_suggestions)
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
