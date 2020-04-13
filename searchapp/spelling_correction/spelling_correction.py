import os
import numpy as np
import heapq
from searchapp.index_and_dict import indexAccess, indexAndDictBuilder
from searchapp.cor_access import corpus_enum
import re
from similarity.weighted_levenshtein import WeightedLevenshtein
from similarity.weighted_levenshtein import CharacterSubstitutionInterface

# for testing
insert_costs = np.ones(128, dtype=np.float64)

# inspired by https://pypi.org/project/strsim/#weighted-levenshtein
# lower substitution costs for vowels
class CharacterSubstitution(CharacterSubstitutionInterface):
    def cost(self, c0, c1):
        if c0 in 'aeiou' and c1 in 'aeiou':
            return 0.5
        return 1.0

# inspired by https://docs.python.org/3/library/heapq.html#heapq.nsmallest
def construct_heap(index, input):
    h = []
    weighted_levenshtein = WeightedLevenshtein(CharacterSubstitution())

    for value in index:
        try:
            pattern = re.compile('[\W_]*[0-9]*', re.UNICODE) # inspired by https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python
            value = pattern.sub('', value)
            dist = weighted_levenshtein.distance(input, value)
        except:
            continue
        heapq.heappush(h, (dist, value))
    return h

def correct_spelling(token, index):
    h = construct_heap(index, token)
    corrected_token = heapq.heappop(h)[1]

    print("Spelling Correction: corrected " + token + " to " + corrected_token)

    return corrected_token

def check_spelling_bool(query, corpus):
    query_list = query.split(' ')
    corrected_query = query_list[:]
    spelling_error = False

    if corpus is corpus_enum.Corpus.COURSES:
        file_name = 'courseIndex.json'
    elif corpus is corpus_enum.Corpus.REUTERS:
        file_name = 'reutersIndex.json'

    path_to_index = os.path.join(os.getcwd(), 'searchapp','index_and_dict', file_name)
    index = indexAccess.getInvertedIndex(path_to_index=path_to_index)

    for i, term in enumerate(query_list):
        front_pars_num = term.count('(')
        term = term.replace('(', '')
        rear_pars_num = term.count(')')
        term = term.replace(')', '')

        if term == 'AND' or term == 'OR' or term == 'AND_NOT' or "*" in term:
            continue

        processed_term, ok = indexAndDictBuilder.preprocToken(term, stopword=False, stem=True, norm=True)
        if processed_term not in index:
            spelling_error = True
            corrected_term = correct_spelling(term, index)

            if front_pars_num > 0:
                term_par = ''
                for x in range(front_pars_num):
                    term_par += '('
                term_par += corrected_term
            elif rear_pars_num > 0:
                term_par = corrected_term
                for x in range(rear_pars_num):
                    term_par += ')'
            else:
                term_par = corrected_term

            corrected_query[i] = term_par

    if spelling_error:
        return ' '.join(corrected_query)
    return None

def check_spelling_vsm(query, corpus):
    query_list = query.split(' ')
    corrected_query = query_list[:]
    spelling_error = False

    if corpus is corpus_enum.Corpus.COURSES:
        file_name = 'courseIndex.json'
    elif corpus is corpus_enum.Corpus.REUTERS:
        file_name = 'reutersIndex.json'

    path_to_index = os.path.join(os.getcwd(), 'searchapp','index_and_dict', file_name)
    index = indexAccess.getInvertedIndex(path_to_index=path_to_index)

    for i, term in enumerate(query_list):
        processed_term, ok = indexAndDictBuilder.preprocToken(term, stopword=False, stem=True, norm=True)
        if processed_term not in index:
            spelling_error = True
            corrected_term = correct_spelling(term, index)
            corrected_query[i] = corrected_term

    if spelling_error:
        return ' '.join(corrected_query)
    return None
