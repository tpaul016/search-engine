from bs4 import BeautifulSoup
from os import listdir, getcwd, chdir
import nltk
import fileinput
import string
import logging
import json
import re
from .. langproc import langProcess
logging.basicConfig(filename='index.log', level=logging.DEBUG)

def serializeIndex(path, inverIndex):
    # Serialize to JSON
    currDir = getcwd()
    chdir(path)
    with open('index.json', 'w') as f:
        json.dump(inverIndex, f, indent=2, sort_keys=True)
    chdir(currDir)

def isDocMapInDocList(docName, docList):
    for doc in docList:
        if doc["name"] == docName:
            return True
    return False

def normTf(maxTfDict, inverIndex):
    """ Divide each entry in the index by the max Tf
    """
    for token in inverIndex:
        docs = inverIndex[token]["docs"]
        for index, doc in enumerate(docs):
            docId = doc["name"]
            inverIndex[token]["docs"][index]["tf"] /= maxTfDict[docId]
    return inverIndex

def preprocToken(token, stopword, stem, norm):
    stopwords = set(nltk.corpus.stopwords.words("english"))
    stemmer = nltk.stem.porter.PorterStemmer()

    token = langProcess.generalPreProcess(token)
    if norm:
        token = langProcess.normalize(token)
    if stopword and token in stopwords:
        # Skip stop words
        return None, False
        
    if stem:
        token = stemmer.stem(token)
    if token == "":
        return None, False
    return token, True

def buildIndex(path, stopword, stem, norm):
    maxTfDict = {}
    
    # Change cwd to the corpus directory
    currDir = getcwd()
    chdir(path)
    inverIndex = {} 
    fileNameList = listdir()

    # tokenize the course collection
    with fileinput.input(fileNameList) as files:
        for f in files:
            soup = BeautifulSoup(f, "xml")
            desc = soup.desc.string
            if desc is not None:
                tokens = nltk.word_tokenize(desc)
                maxtf = 0
                for token in tokens:
                    token, ok = preprocToken(token, stopword, stem, norm)
                    if not ok:
                        continue
                        
                    if len(token) == 1:
                        # Don't want word that's only puncuation
                        if token in string.punctuation:
                            continue
                    elif token not in inverIndex:
                        # If we don't have the token then add it
                        newTf = 1
                        inverIndex[token] = {"docFreq": 1, \
                                "docs": [{"name": files.filename(), "tf": 1}]}
                    elif token in inverIndex:

                        # Check that we haven't already added this document 
                        # to the tokens doc list
                        if not isDocMapInDocList(files.filename(), inverIndex[token]["docs"]):
                            newTf = 1
                            inverIndex[token]["docFreq"] += 1
                            inverIndex[token]["docs"].append({"name": files.filename(), "tf": newTf})

                        # If document has been added, then we need to adjust the tf
                        else:
                            lengthOfDocList = len(inverIndex[token]["docs"]) - 1
                            oldTf = inverIndex[token]["docs"][lengthOfDocList]["tf"] 
                            newTf = oldTf + 1 
                            inverIndex[token]["docs"][lengthOfDocList]["tf"] = newTf

                    if maxtf < newTf:
                        maxtf = newTf
                maxTfDict[files.filename()] = maxtf
        #print(maxTfDict)
        inverIndex = normTf(maxTfDict, inverIndex)

    # Sort each postings list
    for token in inverIndex:
        # Inspired from https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
        inverIndex[token]["docs"] = sorted(inverIndex[token]["docs"], key=lambda k: k['name'])

    chdir(currDir)
    return inverIndex






