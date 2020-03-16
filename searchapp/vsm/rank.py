from .. index_and_dict import indexAccess
import numpy as np
from pandas import DataFrame
import math
from collections import OrderedDict
from .. cor_access import corpusAccess
from .. langproc import langProcess

def buildDF(queryList, inverIndex):
    """Create new DataFrame with entries containing tf weights

    Args:
        queryList: List of query strings
    Returns:
        DataFrame containing tf weights as entries

    """
    # Populates DataFrame with tf values
    df = DataFrame(columns=queryList)
    for query in queryList:
        for doc in inverIndex[query]["docs"]:
            docId = doc["name"]
            if not docId in df.index:
                # Add new row to our DataFrame
                newRow = DataFrame([[0]*len(queryList)], columns=queryList, index=[docId])
                df = df.append(newRow)
            df.loc[docId, query] = doc["tf"]
    #print("original")
    #print(df)
    df = reWeightDataFrame(df, inverIndex)
    #print("reweighted")
    #print(df)
    return df

def preProcQuery(query, inverIndex):
    """Convert query to list of strings and DROPS words not in Index

    Args:
        query: The query string
    Returns:
        Query as list of strings

    """
    queryList = query.split()
    cleanedQueryList = []
    for query in queryList:
        query = langProcess.stem(query)
        if inverIndex.get(query):
            cleanedQueryList.append(query)
        else:
            print("Dropped:", query)
    return cleanedQueryList

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

def reWeightDataFrame(df, inverIndex):
    """Create new DataFrame with entries containing tf-idf weights

    Args:
        df: The original DataFrame with tf values
    Returns:
        DataFrame containing tf-idf weights

    """
    reWeightedDf = DataFrame(index=df.index, columns=df.columns)
    N, columns = df.shape
    for index, row in df.iterrows():
        for column in df.columns:
            docFreq = inverIndex[column]["docFreq"]
            tf = df.loc[row.name, column]
            reWeightedDf.loc[row.name, column] = tfidf(tf, N, docFreq)
    return reWeightedDf

def strListToVec(strList):
    """Convert a list of strings to a vector

    Args:
        strList: List of strings 
    Returns:
        List of integers that represent the occurence of 
        each unique word

    """
    ordDict = OrderedDict()
    for word in strList: 
        if ordDict.get(word):
            ordDict[word] += 1
        else:
            ordDict[word] = 1
    queryVec = []
    for value in ordDict.values():
        queryVec.append(value)
    print(queryVec)

    return queryVec

def cosSim(queryVec, docVec):
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

def rank(query, collection):
    """Produce rankings for the query

    Args:
        query: The query string
        collection: The collection you want to search over (reuters, courses)
    Returns:
        List of Dicts {docId:, excerpt:, score:}

    """
    inverIndex = indexAccess.getInvertedIndex('searchapp/index_and_dict/index.json')
    queryList = preProcQuery(query, inverIndex)
    df = buildDF(queryList, inverIndex)
    rows, columns = df.shape
    queryVec = strListToVec(queryList)
    rankedDictList = []

    first = True
    for index, row in df.iterrows():
        docVec = row.to_numpy()
        score = cosSim(queryVec, docVec)
        docId = row.name.split(".")[0]
        excerpt = corpusAccess.getDocExcerpt(docId)
        newDict = {"docId": docId, "excerpt": excerpt, "score": score} 
        rankedDictList.append(newDict)

    # Inspired from https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
    rankedDictList = sorted(rankedDictList, key=lambda k: k['score'], reverse=True)
     
    return(rankedDictList[0:10])

