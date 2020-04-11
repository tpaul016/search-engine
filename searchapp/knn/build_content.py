from .. cor_access import corpusAccess, corpus_enum
from .. index_and_dict import indexAndDictBuilder as ind
import nltk
from os import chdir, getcwd, listdir
import json

def build_content():
    path = "searchapp/cor_pre_proc/reuters/processed/"
    currDir = getcwd()
    chdir(path)
    fileNameList = listdir()
    chdir(currDir)

    contents_map = {}

    for f in fileNameList:
        docId = f.split(".")[0]
        query = ""
        doc = corpusAccess.getDoc(docId, corpus_enum.Corpus.REUTERS)
        body = doc["body"] 
        tokens = nltk.word_tokenize(body)
        for token in tokens:
            # Apply same preprocessing as inverted index
            token, ok = ind.preprocToken(token, True, True, True)
            if not ok:
                continue
            query += " " + token
        excerpt = corpusAccess.getDocExcerpt(docId, corpus_enum.Corpus.REUTERS)
        tokens = nltk.word_tokenize(excerpt)
        excerpt_str = ""
        for token in tokens:
            # Apply same preprocessing as inverted index
            token, ok = ind.preprocToken(token, True, True, True)
            if not ok:
                continue
            excerpt_str += " " + token
        contents_map[docId] = {}

        topics = doc["topics"]

        if topics is None:
            topics = None
        else:
            if "," in topics:
                topics = topics.split(",")
            else:
                topics = [topics]


        contents_map[docId]["content"] = query
        contents_map[docId]["excerpt"] = excerpt_str
        contents_map[docId]["topics"] = topics

    currDir = getcwd()
    chdir("searchapp/knn/")
    with open("content_map.json", 'w') as f:
        json.dump(contents_map, f, indent=2, sort_keys=True)
    chdir(currDir)
    
        

