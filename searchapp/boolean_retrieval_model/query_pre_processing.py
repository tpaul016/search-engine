from searchapp.index_and_dict import indexAccess
import os
from searchapp.cor_access import corpusAccess

# inspired by https://runestone.academy/runestone/books/published/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
def query_to_postfix(query):
    new_query = []
    op_stack = []
    query = query.split(' ')

    # wildcard managment
    for i, word in enumerate(query):
        if '*' in word:
            front_pars_num = word.count('(')
            if front_pars_num > 0:
                word = word.replace('(', '')
            rear_pars_num = word.count(')')
            if rear_pars_num > 0:
                word = word.replace(')', '')

            formatted_words = handle_wildcard(word)
            if len(formatted_words) == 0:
                query[i] = None
            for j, f_word in enumerate(formatted_words):
                if j == 0:
                    pars = ''
                    if len(formatted_words) == 1 and rear_pars_num > 0:
                        for x in range(rear_pars_num):
                            pars += ')'
                        query[i] = f_word + pars
                    elif front_pars_num > 0:
                        for x in range(front_pars_num):
                            pars += '('
                        query[i] = pars + f_word
                    else:
                        query[i] = f_word
                else:
                    if j == len(formatted_words)-1 and rear_pars_num > 0:
                        pars = ''
                        for x in range(rear_pars_num):
                            pars += ')'
                        f_word += pars
                    query.insert(i+j, f_word)

    for token in query:
        if token == 'AND' or token == 'OR' or token == 'AND_NOT':
            op_stack.append(token)
        elif '(' in token:
            par_count = token.count('(')
            token = token.replace('(', '')
            new_query.append(token)
            for i in range(par_count):
                op_stack.append('(')
        elif ')' in token:
            par_count = token.count(')')
            token = token.replace(')', '')
            new_query.append(token)

            for i in range(par_count):
                top_of_stack = op_stack.pop()
                while top_of_stack != '(':
                    new_query.append(top_of_stack)
                    top_of_stack = op_stack.pop()
        else:
            new_query.append(token)

    for i in range(len(op_stack)):
        new_query.append(op_stack.pop())

    return new_query

def get_query_documents(query):
    query = query_to_postfix(query)
    formatted_query = []

    path_to_index = os.path.join(os.getcwd(), 'searchapp', 'index_and_dict', 'index.json')
    index = indexAccess.getInvertedIndex(path_to_index=path_to_index)

    for token in query:
        if token == 'AND' or token == 'OR' or token == 'AND_NOT':
            formatted_query.append(token)
        else:
            try:
                docs = []
                for doc in index[token]['docs']:
                    doc_entry = {}
                    doc_entry['docId'] = doc['name'].split(".")[0]
                    doc_entry['excerpt'] = corpusAccess.getDocExcerpt(doc_entry['docId'])
                    doc_entry['score'] = 1
                    docs.append(doc_entry)
                formatted_query.append(docs)
            except:
                print(token + ' not in the index')

    return formatted_query

def handle_wildcard(word):
    bigrams = create_bigrams(word)

    path_to_index = os.path.join(os.getcwd(), 'searchapp', 'index_and_dict', 'biIndex.json')
    bi_index = indexAccess.get_bigram_index(path_to_index=path_to_index)

    try:
        terms = (bi_index[bigrams[0]])
        for i in range(1, len(bigrams)):
            bi_terms = bi_index[bigrams[i]]
            common_terms = set(terms) & set(bi_terms)
            terms = list(common_terms)
    except:
        print('no terms match ' + word)
        terms = []

    if len(terms) > 1:
        terms = format_wildcard_terms(terms)

    print('wildcard expanded to:')
    print(terms)
    return terms

def create_bigrams(word):
    word_chars = list(word)
    bigrams = []
    if word_chars[0] != '*':
        bigrams.append('$' + word_chars[0])
    for i in range(1, len(word_chars)):
        if word_chars[i] == '*' or word_chars[i-1] == '*':
            continue
        else:
            bigrams.append(word_chars[i-1] + word_chars[i])
    if word_chars[len(word_chars)-1] != '*':
        bigrams.append(word_chars[len(word_chars)-1] + '$')

    return bigrams

def format_wildcard_terms(terms):
    formatted_terms = []
    num_pars = len(terms) - 1
    pars = ''
    for i in range(num_pars):
        pars += '('
    formatted_terms.append(pars + terms[0])
    for i in range(1, len(terms)):
        formatted_terms.append('OR')
        formatted_terms.append(terms[i] + ')')

    return formatted_terms