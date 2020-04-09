from bs4 import BeautifulSoup
from os import listdir, getcwd, chdir
import nltk
import fileinput
import string
import logging
import json
import re
import math
from .. langproc import langProcess
from .. cor_access import corpus_enum
logging.basicConfig(filename='index.log', level=logging.DEBUG)

def serializeIndex(path, inverIndex, fileName):
    # Serialize to JSON
    currDir = getcwd()
    chdir(path)
    with open(fileName, 'w') as f:
        json.dump(inverIndex, f, indent=2, sort_keys=True)
    chdir(currDir)


def isDocMapInDocList(docName, docList):
    for doc in docList:
        if doc["name"] == docName:
            return True
    return False


def normTf(maxTfDict, inverIndex, N):
    """ Divide each entry in the index by the max Tf
        Also add tfidf
    """
    for token in inverIndex:
        docs = inverIndex[token]["docs"]
        for index, doc in enumerate(docs):
            docId = doc["name"]
            inverIndex[token]["docs"][index]["tf"] /= maxTfDict[docId]
            tf = inverIndex[token]["docs"][index]["tf"]
            df = inverIndex[token]["docFreq"]
            inverIndex[token]["docs"][index]["tfidf"] = tfidf(tf, N, df)
    return inverIndex


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


def preprocToken(token, stopword, stem, norm):
    stopwords = set(nltk.corpus.stopwords.words("english"))

    token = langProcess.generalPreProcess(token)
    if norm:
        token = langProcess.normalize(token)
    if stopword and token in stopwords:
        # Skip stop words
        return None, False
        
    if stem:
        token = langProcess.stem(token)
    if token == "":
        return None, False

    # Don't want word that's only puncuation
    allPunc = True
    for char in token:
        if char not in string.punctuation:
            allPunc = False
    if allPunc:
        return None, False

    return token, True


def buildIndex(corpus, stopword, stem, norm):
    print("Building Inverted Index ...")
    maxTfDict = {}
    
    # Change cwd to the corpus directory
    path = "searchapp/cor_pre_proc/" + corpus.value
    currDir = getcwd()
    chdir(path)
    inverIndex = {}
    fileNameList = listdir()

    for path in fileNameList:
        with open(path) as f:
            soup = BeautifulSoup(f, "xml")

            if corpus == corpus_enum.Corpus.COURSES:
                desc = soup.desc.string
            elif corpus == corpus_enum.Corpus.REUTERS:
                desc = soup.body.string

            if desc is not None:
                tokens = nltk.word_tokenize(desc)
                maxtf = 0
                for token in tokens:
                    token, ok = preprocToken(token, stopword, stem, norm)
                    if not ok:
                        continue

                    if token not in inverIndex:
                        # If we don't have the token then add it
                        newTf = 1
                        inverIndex[token] = {"docFreq": 1, \
                                "docs": [{"name": path, "tf": 1, "tfidf": 0}]}
                    elif token in inverIndex:

                        # Check that we haven't already added this document
                        # to the tokens doc list
                        if not isDocMapInDocList(path, inverIndex[token]["docs"]):
                            newTf = 1
                            inverIndex[token]["docFreq"] += 1
                            inverIndex[token]["docs"].append({"name": path, "tf": newTf, "tfidf": 0})

                        # If document has been added, then we need to adjust the tf
                        else:
                            lengthOfDocList = len(inverIndex[token]["docs"]) - 1
                            oldTf = inverIndex[token]["docs"][lengthOfDocList]["tf"] 
                            newTf = oldTf + 1 
                            inverIndex[token]["docs"][lengthOfDocList]["tf"] = newTf

                    if maxtf < newTf:
                        maxtf = newTf
                maxTfDict[path] = maxtf
    #print(maxTfDict)
    N = len(fileNameList)
    inverIndex = normTf(maxTfDict, inverIndex, N)

    # Sort each postings list
    for token in inverIndex:
        # Inspired from https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
        inverIndex[token]["docs"] = sorted(inverIndex[token]["docs"], key=lambda k: k['name'])

    chdir(currDir)
    print("Finished building Inverted Index")
    return inverIndex






