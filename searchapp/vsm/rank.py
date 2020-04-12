from .. index_and_dict import indexAccess
import numpy as np
from pandas import DataFrame, Series
import math
import re
from collections import OrderedDict
from .. cor_access import corpusAccess, corpus_enum
from .. langproc import langProcess
from searchapp.spelling_correction import spelling_correction
from .. knn import classified_acc as class_acc
from .. relevance_feedback import relevance_index_access as relev

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


def preproc_query(query, inverIndex, corpus):
    """ Convert query to list of strings and a vector

    Args:
        query: The query string
    Returns:
        Query as list of strings

    """
    query_list = query.split()
    ord_dict = OrderedDict()
    spelling_error = False

    for index, word in enumerate(query_list):
        # Handle weights in query string
        word = langProcess.stem(word)
        if inverIndex.get(word):
            if ord_dict.get(word):
                ord_dict[word] += 1
            else:
                ord_dict[word] = 1
        else:
            # spell correction
            word, corrected_query = spelling_correction.correct_spelling(token=word, query=query if not spelling_error else corrected_query, corpus=corpus,
                                                                          model='vsm')
            spelling_error = True

            if ord_dict.get(word):
                ord_dict[word] += 1
            else:
                ord_dict[word] = 1

    cleaned_query_list = []
    query_vector = []
    for key, value in ord_dict.items():
        cleaned_query_list.append(key)
        query_vector.append(value)

    if spelling_error:
        return cleaned_query_list, query_vector, corrected_query
    return cleaned_query_list, query_vector, None

def preproc_weighted_query(query, inverIndex, corpus):
    """ Convert weighted query to list of strings and a vector

    Args:
        query: The query string
    Returns:
        Query as list of strings

    """
    query_list = query.split()
    ord_dict = OrderedDict()
    spelling_error = False

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
                # spell correction
                word, corrected_query = spelling_correction.correct_spelling(token=word, query=query if not spelling_error else corrected_query, corpus=corpus,
                                                                             model='vsm')
                spelling_error = True
                if ord_dict.get(word):
                    ord_dict[word] += 1
                else:
                    ord_dict[word] = 1

    cleaned_query_list = []
    query_vector = []
    for key, value in ord_dict.items():
        cleaned_query_list.append(key)
        query_vector.append(value)

    if spelling_error:
        return cleaned_query_list, query_vector, corrected_query
    return cleaned_query_list, query_vector, None

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


def get_sum(docs, df, length):
    sum = Series([])
    if length > 0:
        for doc in docs:
            sum = sum.add(df.loc[doc + ".xml"], fill_value=0)
        return sum
    else:
        return [0]*length
    
    


def adjust_weight(original_query, query_vec, corpus, alpha, beta, gamma, df):
    """
        Rocchio
    """

    relev_index = relev.get_relevance_index()
    if relev_index.get(original_query):
        rel_docs_list = relev_index[original_query]["relevantDocs"][corpus]
        nonrel_docs_list = relev_index[original_query]["nonRelevantDocs"][corpus]
        num_rel_docs = len(rel_docs_list)
        num_non_rel = len(nonrel_docs_list)

        if num_rel_docs > 0 or num_non_rel > 0:
            # Sum the tf-idfs of all the relevent and nonrelevant
            # documents
            rel_sum = get_sum(rel_docs_list, df, num_rel_docs)
            non_rel_sum = get_sum(nonrel_docs_list, df, num_non_rel)
            
            term2 = []
            term3 = []
            for rel_tfidf, non_rel_tfidf in zip(rel_sum, non_rel_sum):
                if num_rel_docs > 0:
                    # Create term2 vector
                    # beta*(1/|Dr|)*Sum{dj in rel}(dj)
                    term2.append(rel_tfidf * beta * (1/num_rel_docs))
                else:
                    term2.append(0)
                if num_non_rel > 0:
                    # Create term3 vector
                    # gamma*(1/|Dnr|)*Sum{dj in non rel}(dj)
                    term3.append(-non_rel_tfidf * gamma * (1/num_non_rel))
                else:
                    term3.append(0)

            # Create term 1 vector
            # alpha * q0
            term1 = [num * alpha for num in query_vec]
            #print("Rocchio:") 
            #print("term1:", term1)
            #print("term2:", term2)
            #print("term3:", term3)
            # Sum the terms
            result = [t1 + t2 + t3 for t1, t2, t3 in zip(term1, term2, term3)]

            return result
        else:
            # If theres no relevant or non relevant documents then don't adjust
            print("Rocchio: No relevant or non-relevant documents")
            return query_vec
    print("Rocchio: No matching query")
    return query_vec


def rank(query, original_query, amount, corpus, need_topics, topics):
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
        corpus_str = "courses"
    elif corpus is corpus_enum.Corpus.REUTERS:
        file_name = 'reutersIndex.json'
        corpus_str = "reuters"

    alpha, beta, gamma = relev.get_constants(corpus)
    print("alpha", alpha, "beta:", beta, "gamma:", gamma)

    inverIndex = indexAccess.getInvertedIndex('searchapp/index_and_dict/' + file_name)
    if "(" in query:
        # Weighted Query
        query_list, query_vec, corrected_query = preproc_weighted_query(query, inverIndex, corpus)
    else:
        # Unweighted query
        query_list, query_vec, corrected_query = preproc_query(query, inverIndex, corpus)
    #print(query_list, query_vec)
    df = buildDF(query_list, inverIndex, need_topics)
    rows, columns = df.shape
    rankedDictList = []
    query_vec = adjust_weight(original_query, query_vec, corpus_str, alpha, beta, gamma, df)
    print("query list:", query_list)
    print("query vector:", query_vec)

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
    result = []

    # Check if docs have any of the topics
    if len(topics) >0:
        count = 0
        doc_map = class_acc.get_doc_map()
        for doc in rankedDictList:
            if class_acc.has_topic(topics, doc["docId"], doc_map):
                result.append(doc)
                count = count + 1
                if count == amount:
                    break
    else:
        result = rankedDictList[0:amount]

    return(result, corrected_query)
