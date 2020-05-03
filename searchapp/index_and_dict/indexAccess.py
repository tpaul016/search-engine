import json
import os
from searchapp.cor_access import corpus_enum


def getInvertedIndex(corpus: corpus_enum.Corpus):
    if corpus is corpus_enum.Corpus.COURSES:
        file_name = 'courseIndex.json'
    elif corpus is corpus_enum.Corpus.REUTERS:
        file_name = 'reutersIndex.json'
    else:
        print("Error: invalid corpus provided")
        file_name = ""

    path_to_index = os.path.join(os.getcwd(), 'searchapp', 'index_and_dict', file_name)

    with open(path_to_index, 'r') as f:
        inverIndex = json.load(f)
    return inverIndex


def get_bigram_index(corpus: corpus_enum.Corpus):
    if corpus is corpus_enum.Corpus.COURSES:
        file_name = 'courseBiIndex.json'
    elif corpus is corpus_enum.Corpus.REUTERS:
        file_name = 'reutersBiIndex.json'
    else:
        print("Error: invalid corpus provided")
        file_name = ""

    path_to_index = os.path.join(os.getcwd(), 'searchapp', 'index_and_dict', file_name)

    with open(path_to_index, 'r') as f:
        bi_index = json.load(f)
    return bi_index

def get_bigram_model(corpus: corpus_enum.Corpus):
    if corpus == corpus_enum.Corpus.COURSES:
        bigram_path = 'searchapp/bigram_language_model/courses_bigram_language_model.json'
    elif corpus == corpus_enum.Corpus.REUTERS:
        bigram_path = 'searchapp/bigram_language_model/reuters_bigram_language_model.json'
    else:
        print("Error: invalid corpus provided")
        bigram_path = ""

    with open(bigram_path, 'r') as f:
        bigram_model = json.load(f)
    return bigram_model
