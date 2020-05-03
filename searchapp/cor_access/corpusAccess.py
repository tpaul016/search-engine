import os
import re
import sys
from nltk.data import load
from bs4 import BeautifulSoup
from .corpus_enum import Corpus


def parse_courses_docId(docId):
    # matches will contain ['charstring', 'number']
    match = re.match('([a-zA-Z]+)([0-9]+)', docId)
    # TODO: Add error handling if docId is incorrect
    if match is None:
        print("corpusAccess: Regex got no match!!!")

    lower_department = match.group(1).lower()
    return lower_department + match.group(2)


def get_doc(docId, corpus):
    if corpus == Corpus.COURSES:
        new_docId = parse_courses_docId(docId)
        file_path = "corpus"
    elif corpus == Corpus.REUTERS:
        new_docId = docId
        file_path = "reuters/processed"
    else:
        # Should never hit this
        print("corpusAccess: Fatal error no match")
        sys.exit(-1)

    file_ending = ".xml"
    file_name = new_docId + file_ending
    path_to_corpus = os.path.join(os.getcwd(), 'searchapp', 'cor_pre_proc', file_path, file_name)

    with open(path_to_corpus) as f:
        soup = BeautifulSoup(f, "xml")

    if corpus == Corpus.COURSES:
        document = {
            "docId": new_docId,
            "title": soup.title.string,
            "descr": soup.desc.string
        }
    elif corpus == Corpus.REUTERS:
        document = {
            "docId": new_docId,
            "title": soup.title.string,
            "topics": soup.topics.string,
            "body": soup.body.string
        }
    else:
        # Should never hit this
        sys.exit(-1)

    return document


def get_contents_reuters(docId):
    doc = get_doc(docId, Corpus.REUTERS)

    return doc["body"]


def get_topics_reuters(docId):
    doc = get_doc(docId, Corpus.REUTERS)

    return doc["topics"]


def get_doc_excerpt(docId, corpus):
    doc = get_doc(docId, corpus)

    if corpus == Corpus.COURSES:
        text = doc["descr"]
    elif corpus == Corpus.REUTERS:
        text = doc["body"]
    else:
        # Should never hit this
        sys.exit(-1)

    # https://www.nltk.org/api/nltk.tokenize.html
    # Create sentence classifier
    sent_detector = load('tokenizers/punkt/english.pickle')
    excerpt = sent_detector.tokenize(text)[0]

    return excerpt


def get_doc_list(doc_id_list, corpus):
    document_list = []
    for docId in doc_id_list:
        document_list.append(get_doc(docId, corpus))
    return document_list
