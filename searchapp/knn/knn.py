from searchapp.cor_access import corpusAccess, corpus_enum
from searchapp.vsm import rank as vsm
from searchapp.index_and_dict import indexAndDictBuilder as ind
from multiprocessing import Pool
from collections import Counter
from os import chdir, listdir, getcwd
import nltk
import json

def knn():
    """
        Classify all of our documents
        Writes to file each document and its classified or already set topic
    """
    path = "searchapp/cor_pre_proc/reuters/processed/"
    currDir = getcwd()
    chdir(path)
    fileNameList = listdir()
    chdir(currDir)

    # Seperate files into testing (no topic) and training (has topic) sets
    training_set = []
    testing_set = []
    for f in fileNameList:
        doc_id = f.split(".")[0]
        topic = corpusAccess.getTopicsReuters(doc_id)
        if topic is None:
            testing_set.append(doc_id)
        else:
            training_set.append(doc_id)

    # Classify all documents in testing_set
    topics_map = {}
    with Pool() as pool:
        one_doc = pool.map(classify, testing_set, 30)
        for f, topics in one_doc:
            topics_map[f] = topics

    # Add all the courses in the training set
    for doc in training_set:
        topic = corpusAccess.getTopicsReuters(doc)
        if topic is None:
            print("Doc with no topic in training set!")
            break
        if "," in topic:
            topics_map[doc] = topic.split(",")
        else:
            topics_map[doc] = [topic]

    with open("searchapp/knn/classified_docs.json", 'w') as f:
        json.dump(topics_map, f, indent=2, sort_keys=True)


def classify(f):
    """
        Classify one document
    """
    query = ""
    body = corpusAccess.getContentsReuters(f)
    tokens = nltk.word_tokenize(body)
    for token in tokens:
        # Apply same preprocessing as inverted index
        token, ok = ind.preprocToken(token, True, True, True)
        if not ok:
            continue
        query += " " + token

    # Input body of our document as the query to VSM 
    # to get the similarity to every other document
    # 
    # need_topics is set to True to ensure VSM only 
    # ranks documents with topics (in our training set)
    #
    # We ask for the top 5 documents (k = 5)
    ranking = vsm.rank(query, 5, corpus_enum.Corpus.REUTERS, True, [])

    cand_topics = []
    # Get all the topics from our 5 documents
    for doc in ranking:
        topic = corpusAccess.getTopicsReuters(doc["docId"])
        if topic is None:
            continue
        # We get the topics as a string
        # Must split on comma to get each topic
        if "," in topic:
            new_cand_topics = topic.split(",")
            cand_topics += new_cand_topics
        else:
            cand_topics.append(topic)

    # From all of our topics take the topic that occurs the most
    c = Counter(cand_topics)
    tuple_topics = c.most_common(1)
    # The list comprehension is if we wanted to 
    # classify our documents with more then one topic
    topics = [t for t, count in tuple_topics]
    return f, topics


