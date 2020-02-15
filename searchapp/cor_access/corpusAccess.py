import os
import re
from bs4 import BeautifulSoup

def parseDocId(docId):
    # matches will contain ['charstring', 'number']
    match = re.match('([a-zA-Z]+)([0-9]+)', docId)
    # TODO: Add error handling if docId is incorrect
    assert not match == None
    lowerDepartment = match.group(1).lower()
    return lowerDepartment + match.group(2)

def getDoc(docId):
    newDocId = parseDocId(docId)
    fileName = newDocId + ".xml"
    path_to_corpus = os.path.join(os.getcwd(), 'searchapp', 'cor_pre_proc', 'corpus', fileName)

    with open(path_to_corpus) as f:
        soup = BeautifulSoup(f, "xml")

    document = {
        "docId": newDocId,
        "title": soup.title.string,
        "descr": soup.desc.string
    }

    return document

def getDocExcerpt(docId):
    doc = getDoc(docId)
    excerpt = doc["descr"].partition(".")[0]
    return excerpt + "."

def getDocList(docIdList):
    documentList = [] 
    for docId in docIdList:
        documentList.append(getDoc(docId))
    return documentList

        
        




