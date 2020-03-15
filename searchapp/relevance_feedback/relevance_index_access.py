relevance_index = {}

def update(query, docId, type, checked):
    global relevance_index
    if query in relevance_index:
        if docId in relevance_index[query][type]:
            if checked:
                relevance_index[query][type].append(docId)
            else:
                relevance_index[query][type].remove(docId)
        elif checked:
            relevance_index[query][type].append(docId)
    else:
        relevance_index[query] = {}
        relevance_index[query]['relevantDocs'] = []
        relevance_index[query]['nonRelevantDocs'] = []
        if checked:
            relevance_index[query][type].append(docId)

    print("------------relevance index-----------------")
    print(relevance_index)
