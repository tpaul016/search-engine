from .. index_and_dict import indexAccess
import numpy as np
from pandas import DataFrame
import math
import re
from collections import OrderedDict
from .. cor_access import corpusAccess, corpus_enum
from .. langproc import langProcess


def buildDF(query_list, inverIndex, need_topics):
    """Create new DataFrame with entries containing tfidf weights

    Args:
        queryList: List of query strings
    Returns:
        DataFrame containing tfidf weights as entries

    """

    query_map = {}
    for i, word in enumerate(query_list):
        query_map[word] = i

    # Keep map of doc_ids to indicies
    index_map = {}
    index = []

    # Create a dataframe from this later
    temp_arr = []

    # Store all tfidf values in tmp_arr
    for word in query_list:
        for doc in inverIndex[word]["docs"]:
            doc_id = doc["name"]
            
            # Only interested in documents that have topics (kNN)
            if need_topics:
                split_doc_id = doc_id.split(".")[0]
                topic = corpusAccess.getTopicsReuters(split_doc_id)
                if topic is None:
                    continue

            if not index_map.get(doc_id):
                # Add new row to our temp array
                new_row = [0] * len(query_list)
                temp_arr.append(new_row)
                index_map[doc_id] = len(index)
                index.append(doc_id)

            doc_id_index = index_map[doc_id]
            query_index = query_map[word]

            temp_arr[doc_id_index][query_index] = doc["tfidf"]
    df = DataFrame(data=temp_arr, index=index, columns=query_list)
    return df


def preproc_query(query, inverIndex):
    """ Convert query to list of strings and a vector

    Args:
        query: The query string
    Returns:
        Query as list of strings

    """
    query_list = query.split()
    ord_dict = OrderedDict()

    for index, word in enumerate(query_list):
        # Handle weights in query string
        word = langProcess.stem(word)
        if inverIndex.get(word):
            if ord_dict.get(word):
                ord_dict[word] += 1
            else:
                ord_dict[word] = 1
        #else:
        #    print("Dropped:", word)
            
    cleaned_query_list = []
    query_vector = []
    for key, value in ord_dict.items():
        cleaned_query_list.append(key)
        query_vector.append(value)
    return cleaned_query_list, query_vector

def preproc_weighted_query(query, inverIndex):
    """ Convert weighted query to list of strings and a vector

    Args:
        query: The query string
    Returns:
        Query as list of strings

    """
    query_list = query.split()
    ord_dict = OrderedDict()

    for index, elem in enumerate(query_list):
        if '(' in elem:
            # Handle weights in query string
            elem = re.sub(r"\(|\)", "", elem)
            word = langProcess.stem(query_list[index - 1])
            if inverIndex.get(word):
                if ord_dict.get(word):
                    ord_dict[word] += float(elem)
                else:
                    ord_dict[word] = float(elem)
            else:
                print("Dropped:", elem)

    cleaned_query_list = []
    query_vector = []
    for key, value in ord_dict.items():
        cleaned_query_list.append(key)
        query_vector.append(value)
    return cleaned_query_list, query_vector

def tfidf(tf, N, docFreq):
    """Calculate tf-idf value

    N + 1

    Args:
        tf: The NORMALIZED (by max tf) term frequency value of the word in the document
        N: The amount of documents
        docFreq: The document frequency of the word
    Returns:
        Calculated tf-idf weighting

    """
    #weight = math.log(1 + tf, 10) * math.log((N+1)/docFreq)
    weight = tf * math.log((N+1)/docFreq, 10)
    return weight


def cosSim(queryVec, docVec, file_name):
    """Calculate the cosine similarity of two vectors

    Args:
        queryVec: vector 1
        docVec: vector 2
    Returns:
        The cosine similarity of the two vectors

    """
    # Inspired by http://danushka.net/lect/dm/Numpy-basics.html
    cosSim = np.dot(queryVec, docVec) /  \
        (np.sqrt(np.dot(queryVec, queryVec)) * np.sqrt(np.dot(docVec, docVec)))
    return cosSim

def rank(query, amount, corpus, need_topics):
    """Produce rankings for the query

    Args:
        query: The query string
        amount: amount of results
        corpus: The corpus you want to search over (reuters, courses)
    Returns:
        List of Dicts {docId:, excerpt:, score:}

    """
    if corpus is corpus_enum.Corpus.COURSES:
        file_name = 'courseIndex.json'
    elif corpus is corpus_enum.Corpus.REUTERS:
        file_name = 'reutersIndex.json'

    inverIndex = indexAccess.getInvertedIndex('searchapp/index_and_dict/' + file_name)
    if "(" in query:
        # Weighted Query
        query_list, query_vec = preproc_weighted_query(query, inverIndex)
    else:
        # Unweighted query
        query_list, query_vec = preproc_query(query, inverIndex)
    #print(query_list, query_vec)
    df = buildDF(query_list, inverIndex, need_topics)
    rows, columns = df.shape
    rankedDictList = []

    for index, row in df.iterrows():
        docVec = row.to_numpy()
        score = cosSim(query_vec, docVec, corpus)
        docId = row.name.split(".")[0]
        excerpt = corpusAccess.getDocExcerpt(docId, corpus)
        newDict = {"docId": docId, "excerpt": excerpt, "score": score} 
        rankedDictList.append(newDict)

    # Inspired from https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
    rankedDictList = sorted(rankedDictList, key=lambda k: k['score'], reverse=True)

    if amount > len(rankedDictList):
        amount = len(rankedDictList)

    result = rankedDictList[0:amount]

    return(result)

