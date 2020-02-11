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

def buildIndex(path, stopword, stem, norm):
    stopwords = set(nltk.corpus.stopwords.words("english"))
    stemmer = nltk.stem.porter.PorterStemmer()
    # Necessary for word_tokenize()

    # tokenize the course collection
    currDir = getcwd()
    chdir(path)
    inverIndex = {} 
    fileNameList = listdir()
    with fileinput.input(fileNameList) as files:
        for f in files:
            soup = BeautifulSoup(f, "xml")
            desc = soup.desc.string
            if desc is not None:
                # tokenizer = nltk.RegexpTokenizer('\w+|[\w\.]+')
                # token = tokenizer.tokenize(desc)
                tokens = nltk.word_tokenize(desc)
                for token in tokens:
                    token = langProcess.generalPreProcess(token)
                
                    if norm:
                        token = langProcess.normalize(token)
                    if stopword and token in stopwords:
                        # Skip stop words
                        continue
                    if stem:
                        token = stemmer.stem(token)
                    if token == "":
                        continue
                        
                    if len(token) == 1:
                        # Don't want word that's only puncuation
                        if token in string.punctuation:
                            continue
                    elif token not in inverIndex:
                        # If we don't have the token then add it
                        inverIndex[token] = {"docFreq": 1, \
                                "docs": [{"name": files.filename(), "tf": 1}]}
                    elif token in inverIndex:
                        # Check that we haven't already added this document 
                        # to the tokens doc list
                        if not isDocMapInDocList(files.filename(), inverIndex[token]["docs"]):
                            inverIndex[token]["docFreq"] += 1
                            inverIndex[token]["docs"].append({"name": files.filename(), "tf": 1})
                        # If document has been added, then we need to adjust the tf
                        else:
                            lengthOfDocList = len(inverIndex[token]["docs"]) - 1
                            inverIndex[token]["docs"][lengthOfDocList]["tf"] += 1

    # Sort each postings list
    for token in inverIndex:
        # Inspired from https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
        inverIndex[token]["docs"] = sorted(inverIndex[token]["docs"], key=lambda k: k['name'])

    chdir(currDir)
    return inverIndex






