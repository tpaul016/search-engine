#from .langproc import stopword
from bs4 import BeautifulSoup
from os import listdir, getcwd, chdir
import nltk
import fileinput
import string
import logging
import json
logging.basicConfig(filename='index.log',level=logging.DEBUG)

def isDocMapInDocList(docName, docList):
    for doc in docList:
        if doc["name"] == docName:
            return True
    return False

def buildIndex(stopword, stem, norm):
    # Necessary for word_tokenize()
    nltk.download('punkt')

    # tokenize the course collection
    currDir = getcwd()
    inverIndex = {} 
    addToDict = False
    appendToDocs = False
    try:
        # TODO: May need to change this if you reconnect to main app
        chdir("../cor_pre_proc/corpus")
        fileNameList = listdir()
        with fileinput.input(fileNameList) as files:
            for f in files:
                soup = BeautifulSoup(f, "xml")
                desc = soup.desc.string
                if desc is not None:
                    # Need to deal with periods at the end or colons
                    # Should probably do this instead of word_tokenize
                    # tokenizer = nltk.RegexpTokenizer('\w+|[\w\.]+')
                    # inverIndex = termList + tokenizer.tokenize(desc)
                    tokens = nltk.word_tokenize(desc)
                    for token in tokens:

                        if len(token) == 1:
                            if token in string.punctuation:
                                continue
                        elif token not in inverIndex:
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
    finally:
        chdir(currDir)

    # Sort each postings list
    for token in inverIndex:
        # Inspired from https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
        inverIndex[token]["docs"] = sorted(inverIndex[token]["docs"], key=lambda k: k['name'])

    logging.debug(inverIndex)

    # Serialize to JSON 
    with open('index.json', 'w') as f:
        json.dump(inverIndex, f, indent=2, sort_keys=True)

buildIndex(False, False, False)




