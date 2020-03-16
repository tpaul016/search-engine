from nltk import wordnet
import re
import heapq

# inspired by https://www.tutorialspoint.com/how-to-get-synonyms-antonyms-from-nltk-wordnet-in-python
def expand_query(query, N):
    input_terms = query.split(' ')
    expanded_query = ''
    for term in input_terms:
        if term == 'AND' or term == 'OR' or term == 'AND_NOT':
            expanded_query += ' ' + term + ' '
            # suggestions.append([term for i in range(N)])
        else:
            front_par_count = term.count('(')
            back_par_count = term.count(')')
            term = term.replace('(', '')
            term = term.replace(')', '')

            heap = construct_heap(wordnet.synset(term))
            n_synonyms = [heapq.heappop(heap)[1] for i in range(N)]
            n_synonyms = '(' + ' OR '.join(n_synonyms) + ')'

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



        if term not in index:
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

    # formatted_suggestions = format_suggestions(suggestions, len(input_terms), N)
    # return formatted_suggestions
    return suggestions

def construct_heap(synonyms):
    h = []
    for synonym in synonyms:
        similarity = synonyms.wup_similarity(synonym[0].name())
        heapq.heappush(h, (similarity, synonym[0].lemmas()[0].name()))
    return h
