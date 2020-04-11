from searchapp.index_and_dict import indexAccess, indexAndDictBuilder
import os
from searchapp.cor_access import corpusAccess, corpus_enum

# inspired by https://runestone.academy/runestone/books/published/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
def query_to_postfix(query, corpus):
    new_query = []
    op_stack = []
    query = query.split(' ')

    # stemming and wildcard management
    for i, word in enumerate(query[:]):
        if not(word == 'AND' or word == 'OR' or word == 'AND_NOT'):
            front_pars_num = word.count('(')
            if front_pars_num > 0:
                word = word.replace('(', '')
            rear_pars_num = word.count(')')
            if rear_pars_num > 0:
                word = word.replace(')', '')

            if '*' in word:
                formatted_words = handle_wildcard(word, corpus)
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
                        if j == len(formatted_words) - 1 and rear_pars_num > 0:
                            pars = ''
                            for x in range(rear_pars_num):
                                pars += ')'
                            f_word += pars
                        query.insert(i + j, f_word)
            else:
                formatted_word, ok = indexAndDictBuilder.preprocToken(word, stopword=False, stem=True, norm=True)

                if front_pars_num > 0:
                    word_par = ''
                    for i in range(front_pars_num):
                        word_par += '('
                    word_par += formatted_word
                elif rear_pars_num > 0:
                    word_par = formatted_word
                    for i in range(rear_pars_num):
                        word_par += ')'
                else:
                    word_par = formatted_word

                query[i] = word_par

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

def get_query_documents(query, corpus):
    query = query_to_postfix(query, corpus)
    formatted_query = []

    if corpus is corpus_enum.Corpus.COURSES:
        file_name = 'courseIndex.json'
    elif corpus is corpus_enum.Corpus.REUTERS:
        file_name = 'reutersIndex.json'

    path_to_index = os.path.join(os.getcwd(), 'searchapp', 'index_and_dict', file_name)
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
                    doc_entry['excerpt'] = corpusAccess.getDocExcerpt(doc_entry['docId'], corpus)
                    doc_entry['score'] = 1
                    docs.append(doc_entry)
                formatted_query.append(docs)
            except Exception as e:
                print(e)
                print(token + ' not in the index')

    return formatted_query

def handle_wildcard(word, corpus):
    bigrams = create_bigrams(word)

    if corpus is corpus_enum.Corpus.COURSES:
        file_name = 'courseBiIndex.json'
    elif corpus is corpus_enum.Corpus.REUTERS:
        file_name = 'reutersBiIndex.json'

    path_to_index = os.path.join(os.getcwd(), 'searchapp', 'index_and_dict', file_name)
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
