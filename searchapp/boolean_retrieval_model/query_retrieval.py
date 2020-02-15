# inspired by https://runestone.academy/runestone/books/published/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
def execute_query(query):
    query_result = []
    operand_stack = []

    if len(query) == 1:
        return query[0]

    for token in query:
        if token == 'AND' or token == 'OR' or token == 'AND_NOT':
            docs2 = operand_stack.pop()
            docs1 = operand_stack.pop()

            if token == 'AND':
                query_result = operation_AND(docs1, docs2)
            elif token == 'OR':
                query_result = operation_OR(docs1, docs2)
            elif token == 'AND_NOT':
                query_result = operation_AND_NOT(docs1, docs2)

            operand_stack.append(query_result)
        else:
            operand_stack.append(token)

    return query_result

def operation_AND(docs1, docs2):
    new_docs = []
    pointer1 = 0
    pointer2 = 0

    while pointer1 < len(docs1) and pointer2 < len(docs2):
        doc1 = docs1[pointer1]
        doc2 = docs2[pointer2]
        if doc1['docId'] == doc2['docId']:
            new_docs.append(doc1)
            pointer1 += 1
            pointer2 += 1
        else:
            min_pointer = min(doc1['docId'], doc2['docId'])
            if min_pointer == doc1['docId']:
                pointer1 += 1
            if min_pointer == doc2['docId']:
                pointer2 += 1
    return new_docs

def operation_OR(docs1, docs2):
    new_docs = [doc for doc in docs2]
    for doc in docs1:
        if doc not in new_docs:
            new_docs.append(doc)
    return sorted(new_docs, key=lambda k: k['docId'])

def operation_AND_NOT(docs1, docs2):
    new_docs = []
    pointer1 = 0
    pointer2 = 0

    # doc1 AND_NOT doc2
    while pointer1 < len(docs1) and pointer2 < len(docs2):
        doc1 = docs1[pointer1]
        doc2 = docs2[pointer2]
        if doc1['docId'] != doc2['docId']:
            min_pointer = min(doc1['docId'], doc2['docId'])
            if min_pointer == doc1['docId']:
                new_docs.append(doc1)
                pointer1 += 1
            else:
                pointer2 += 1
        else:
            pointer1 += 1
            pointer2 += 1
    return new_docs