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
        inverIndex = json.load(f)
    return inverIndex
