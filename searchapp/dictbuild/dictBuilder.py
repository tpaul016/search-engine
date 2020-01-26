#from .langproc import stopword
from bs4 import BeautifulSoup
from os import listdir, getcwd, chdir
import nltk
import fileinput
import string
import logging
logging.basicConfig(filename='termDict.log',level=logging.DEBUG)

def buildDict(stopword, stem, norm):
    # tokenize the course collection
    currDir = getcwd()
    termDict = {} 
    addToDict = False
    appendToDocs = False
    try:
        chdir("./searchapp/corPreProc/corpus")
        fileNameList = listdir()
        with fileinput.input(fileNameList) as files:
            for f in files:
                soup = BeautifulSoup(f, "xml")
                desc = soup.desc.string
                if(desc is not None):
                    # Need to deal with periods at the end or colons
                    # Should probably do this instead of word_tokenize
                    # tokenizer = nltk.RegexpTokenizer('\w+|[\w\.]+')
                    # termDict = termList + tokenizer.tokenize(desc)
                    tokens = nltk.word_tokenize(desc)
                    for token in tokens:
                        #Perform stopword, normalization, casefolding, stemming somewhere in this loop
                        if len(token) == 1:
                            if token in string.punctuation:
                                continue
                        elif token not in termDict:
                            termDict[token] = {"weight": 0, "docs": [files.filename()]}
                        elif token in termDict:
                            # Check that we haven't already added this document 
                            if(files.filename() not in termDict[token]["docs"]):
                                termDict[token]["docs"].append(files.filename())
    finally:
        chdir(currDir)
    logging.debug(termDict)
    return(termDict)
            




