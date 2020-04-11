import json

def get_doc_map():
    with open("searchapp/knn/classified_docs.json", 'r') as f:
        doc_map = json.load(f)
    return doc_map

def has_topic(topics, doc, doc_map):
    """
        Check if document has one of the topics
    """
    docs_topics = doc_map[doc]
    for top in docs_topics:
        if top in topics:
            return True
    return False