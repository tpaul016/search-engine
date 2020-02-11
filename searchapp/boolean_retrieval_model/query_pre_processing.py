from searchapp.index_and_dict import indexAccess
import os

# inspired by https://runestone.academy/runestone/books/published/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
def query_to_postfix(query):
    new_query = [];
    op_stack = [];
    query = query.split(' ')

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
    query = query_to_postfix(query);
    formatted_query = []

    path_to_index = os.path.join(os.getcwd(), 'searchapp', 'index_and_dict', 'index.json')
    index = indexAccess.getInvertedIndex(path_to_index=path_to_index)

    for token in query:
        if token == 'AND' or token == 'OR' or token == 'AND_NOT':
            formatted_query.append(token)
        else:
            try:
                docs = [doc['name'] for doc in index[token]['docs']]
                formatted_query.append(docs)
            except:
                print(token + ' not in the index')

    return formatted_query