from searchapp.cor_access import corpusAccess, corpus_enum
from . knn_rank import rank
from searchapp.index_and_dict import indexAndDictBuilder as ind
from multiprocessing import Pool
from collections import Counter
from os import chdir, listdir, getcwd
import nltk
import json

contents_map = {}
inverIndex = {}

def knn(index, c_map):
    """
        Classify all of our documents
        Writes to file each document and its classified or already set topic
    """
    global contents_map
    global inverIndex
    contents_map = c_map
    inverIndex = index

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
        topic = contents_map[doc_id]["topics"]
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
        topic = contents_map[doc]["topics"]
        if topic is None:
            print("Doc with no topic in training set!")
            break
        if "," in topic:
            topics_map[doc] = topic.split(",")
        else:
            topics_map[doc] = topic

    with open("searchapp/knn/exp_classified_docs.json", 'w') as f:
        json.dump(topics_map, f, indent=2, sort_keys=True)


def classify(f):
    """
        Classify one document
    """
    global contents_map
    body = contents_map[f]["content"]

    # Input body of our document as the query to VSM 
    # to get the similarity to every other document
    # 
    # need_topics is set to True to ensure VSM only 
    # ranks documents with topics (in our training set)
    #
    # We ask for the top 5 documents (k = 5)
    ranking = rank(body, 5, corpus_enum.Corpus.REUTERS, True, inverIndex, contents_map)
    
    cand_topics = []
    # Get all the topics from our 5 documents
    for doc in ranking:
        topic = contents_map[doc["docId"]]["topics"]
        if topic is None:
            print(doc, "has no topic!")
            break
        elif len(topic) == 0:
            print(doc, "has no topic!")
            break
        cand_topics += topic


    # From all of our topics take the topic that occurs the most
    c = Counter(cand_topics)
    tuple_topics = c.most_common(1)
    # The list comprehension is if we wanted to 
    # classify our documents with more then one topic
    topics = [t for t, count in tuple_topics]
    return f, topics


