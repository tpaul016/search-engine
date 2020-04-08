import os
import re
import sys
from bs4 import BeautifulSoup
from .corpus_enum import Corpus

def parseCoursesDocId(docId):
    # matches will contain ['charstring', 'number']
    match = re.match('([a-zA-Z]+)([0-9]+)', docId)
    # TODO: Add error handling if docId is incorrect
    if match == None:
        print("corpusAccess: Regex got no match!!!")

    lowerDepartment = match.group(1).lower()
    return lowerDepartment + match.group(2)

def parseReutersDocId(docId):
    # matches will contain ['charstring', 'number']
    match = re.match('reuters-', docId)
    # TODO: Add error handling if docId is incorrect
    assert not match == None
    lowerDepartment = match.group(1).lower()
    return lowerDepartment + match.group(2)

def getDoc(docId, corpus):
    if corpus == Corpus.COURSES:
        newDocId = parseCoursesDocId(docId)
    elif corpus == Corpus.REUTERS:
        newDocId = docId
    else:
        # Should never hit this
        print("corpusAccess: Fatal error no match")
        sys.exit(-1)

    file_ending = ".xml"
    fileName = newDocId + file_ending
    path_to_corpus = os.path.join(os.getcwd(), 'searchapp', 'cor_pre_proc', corpus.value, fileName)

    with open(path_to_corpus) as f:
        soup = BeautifulSoup(f, "xml")

    if corpus == Corpus.COURSES:
        document = {
            "docId": newDocId,
            "title": soup.title.string,
            "descr": soup.desc.string
        }
    elif corpus == Corpus.REUTERS:
        document = {
            "docId": newDocId,
            "title": soup.title.string,
            "topics": soup.topics.string,
            "body": soup.body.string
        }
    else:
        # Should never hit this
        sys.exit(-1)

    return document

def getDocExcerpt(docId, corpus):
    doc = getDoc(docId, corpus)

    if corpus == Corpus.COURSES:
        excerpt = doc["descr"].partition(".")[0]
    elif corpus == Corpus.REUTERS:
        excerpt = doc["body"].partition(".")[0]
    else:
        # Should never hit this
        sys.exit(-1)
    return excerpt + "."

def getDocList(docIdList, corpus):
    documentList = []
    for docId in docIdList:
        documentList.append(getDoc(docId, corpus))
    return documentList

        
        




