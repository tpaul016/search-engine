#from .langproc import stopword
from bs4 import BeautifulSoup
from os import listdir, getcwd, chdir
import nltk
import fileinput
import string
import logging
import json
import re # RMME
#from ... langproc import langProcess
logging.basicConfig(filename='index.log',level=logging.DEBUG)

nltk.download('stopwords') #TODO: should move to application setup

def hyphenRemoval(token):
    word = token.replace("-", "")

    if len(word) == 0:
        return(word, False)
    else:
        return(word, True)

    # Matches alphanumericString-alphanumericString
    #matches = re.findall('([a-zA-Z0-9]+)(-)([a-zA-Z0-9]+)', token)
    # matches will contain ['alphanumericString', '-' 'alphanumericString']
    #if len(matches) == 3:
    #    newWord = matches[0] + matches[1]
    #    return(newWord)
    #else:
    #    return(token)

def periodRemoval(token):
    word = token.replace(".", "")

    if len(word) == 0:
        return(word, False)
    else:
        return(word, True)

def isDocMapInDocList(docName, docList):
    for doc in docList:
        if doc["name"] == docName:
            return True
    return False

def buildIndex(stopword, stem, norm):
    stopwords = set(nltk.corpus.stopwords.words("english"))
    stemmer = nltk.stem.porter.PorterStemmer()
    # Necessary for word_tokenize()
    nltk.download('punkt') #TODO: should move to application setup

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
                    
                        if stopword and token in stopwords:
                            continue
                        if norm:
                            # TODO
                            #newToken = langProcess.hyphenRemoval(token)
                            #newToken, okPeriod = langProcess.periodRemoval(token)
                            #RMME
                            newToken, okHyphen = hyphenRemoval(token)
                            if not okHyphen:
                                continue
                            else:
                                token = newToken

                            newToken, okPeriod = periodRemoval(token)
                            if not okPeriod:
                                continue
                            else:
                                token = newToken

                        if stem:
                            token = stemmer.stem(token)
                            
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

buildIndex(True, True, True)




