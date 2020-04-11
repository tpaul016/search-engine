from .. relevance_feedback import relevance_index_access as relev
from .. cor_access import corpus_enum
import json

def local_expan(query, corpus, weight):
    addition = ""
    index = relev.get_relevance_index()
    if index.get(query):
        if corpus is corpus_enum.Corpus.COURSES:
            file_name = 'course_top_tfidf.json'
            corpus_str = "courses"
        elif corpus is corpus_enum.Corpus.REUTERS:
            file_name = 'reuters_top_tfidf.json'
            corpus_str = "reuters"

        relev_docs = index[query]["relevantDocs"][corpus_str]


        with open("searchapp/query_expan/" + file_name, 'r') as f:
            doc_map = json.load(f)

        add_weight = False
        if weight != 0:
            add_weight = True
        
        for doc in relev_docs:
            for word in doc_map[doc + ".xml"]:
                if add_weight:
                    addition += " " + word + " (1)"
                else:
                    addition += " " + word
        return addition
    else:
        return addition
       