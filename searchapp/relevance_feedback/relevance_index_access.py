from .. cor_access import corpus_enum

relevance_index = {}
course_beta = 0.75
course_gamma = 0.15
reuters_beta = 0.75
reuters_gamma = 0.15

def get_relevance_index():
    return relevance_index

def get_constants(corpus):
    if corpus is corpus_enum.Corpus.COURSES:
        return 1, course_beta, course_gamma
    elif corpus is corpus_enum.Corpus.REUTERS:
        return 1, reuters_beta, reuters_gamma
    else:
        print("relevance index constant invalid corpus")

def get_other_type(type):
    return "nonRelevantDocs" if type == "relevantDocs" else "relevantDocs"

def update(query, docId, type, checked, corpus):
    corpus = corpus.strip("/")
    global relevance_index
    global course_beta
    global course_gamma
    global reuters_beta
    global reuters_gamma

    if query in relevance_index:
        if docId in relevance_index[query][type][corpus]:
            if checked:
                relevance_index[query][type][corpus].append(docId)
            else:
                relevance_index[query][type][corpus].remove(docId)
        # Query is in index but new docId is not
        elif checked:
            other_type = get_other_type(type)
            # If user decides document is not relevant anymore or vice versa
            if docId in relevance_index[query][other_type][corpus]:
                relevance_index[query][other_type][corpus].remove(docId)
            # Add to other type
            relevance_index[query][type][corpus].append(docId)
    # Query not in index, create data structure
    else:
        relevance_index[query] = {}
        relevance_index[query]['relevantDocs'] = {}
        relevance_index[query]['relevantDocs']['courses'] = []
        relevance_index[query]['relevantDocs']['reuters'] = []
        relevance_index[query]['nonRelevantDocs'] = {}
        relevance_index[query]['nonRelevantDocs']['courses'] = []
        relevance_index[query]['nonRelevantDocs']['reuters'] = []
        if checked:
            relevance_index[query][type][corpus].append(docId)
    
    print("------------relevance index-----------------")
    print(relevance_index)
    print("course_beta:", course_beta, "| course_gamma:", course_gamma, "| reuters_beta:", reuters_beta, "| reuters_gamma:", reuters_gamma)
