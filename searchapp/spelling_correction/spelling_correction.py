import os
import numpy as np
import heapq
from searchapp.index_and_dict import indexAccess, indexAndDictBuilder
from searchapp.cor_access import corpus_enum
import re
from nltk.metrics import edit_distance

# for testing
insert_costs = np.ones(128, dtype=np.float64)

# inspired by https://docs.python.org/3/library/heapq.html#heapq.nsmallest
def construct_heap(index, input):
    h = []
    for value in index:
        try:
            pattern = re.compile('[\W_]*[0-9]*', re.UNICODE) # inspired by https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python
            value = pattern.sub('', value)
            dist = edit_distance(input, value, substitution_cost=1, transpositions=False)
        except:
            continue
        heapq.heappush(h, (dist, value))
    return h

def correct_query_bool(token, query, corrected_token):
    query_list = query.split(' ')
    for index, term in enumerate(query_list):
        front_pars_num = term.count('(')
        term = term.replace('(', '')
        rear_pars_num = term.count(')')
        term = term.replace(')', '')

        processed_term, ok = indexAndDictBuilder.preprocToken(term, stopword=False, stem=True, norm=True)
        if processed_term == token:
            if front_pars_num > 0:
                term_par = ''
                for i in range(front_pars_num):
                    term_par += '('
                term_par += corrected_token
            elif rear_pars_num > 0:
                term_par = corrected_token
                for i in range(rear_pars_num):
                    term_par += ')'
            else:
                term_par = corrected_token

            query_list[index] = term_par

    return ' '.join(query_list)

def correct_query_vsm(token, query, corrected_token):
    query_list = query.split(' ')
    for index, term in enumerate(query_list):
        processed_term, ok = indexAndDictBuilder.preprocToken(term, stopword=False, stem=True, norm=True)
        if processed_term == token:
            query_list[index] = corrected_token

    return ' '.join(query_list)

def correct_spelling(token, query, corpus, model):
    if corpus is corpus_enum.Corpus.COURSES:
        file_name = 'courseIndex.json'
    elif corpus is corpus_enum.Corpus.REUTERS:
        file_name = 'reutersIndex.json'

    path_to_index = os.path.join(os.getcwd(), 'searchapp','index_and_dict', file_name)
    index = indexAccess.getInvertedIndex(path_to_index=path_to_index)

    h = construct_heap(index, token)
    corrected_token = heapq.heappop(h)[1]

    print("Spelling Correction: corrected " + token + " to " + corrected_token)

    if model == 'vsm':
        corrected_query = correct_query_vsm(token, query, corrected_token)
    elif model == 'bool':
        corrected_query = correct_query_bool(token, query, corrected_token)

    return corrected_token, corrected_query
