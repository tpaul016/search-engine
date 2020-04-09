from .. index_and_dict import indexAccess
import json
from os import getcwd, chdir
from operator import itemgetter

def build():
    build_top_tfidf_map("courseIndex.json", "course_top_tfidf.json")
    build_top_tfidf_map("reutersIndex.json", "reuters_top_tfidf.json")

def build_top_tfidf_map(index_name, out_file_name):
    inverIndex = indexAccess.getInvertedIndex('searchapp/index_and_dict/' + index_name)
    doc_map = {}
    for word, val in inverIndex.items():
        for doc in val["docs"]:
            doc_name = doc["name"]
            word_tfidf = doc["tfidf"]
            if doc_map.get(doc_name):
                doc_map[doc_name].append((word, word_tfidf))
            else:
                doc_map[doc_name] = [(word, word_tfidf)]

    for doc, words in doc_map.items():
        # Sort list and take top 3
        # Inspired from https://docs.python.org/3/howto/sorting.html
        sorted_words = sorted(words, key=lambda w: w[1], reverse=True)
        sorted_words = sorted_words[0:3]
        new_words = []
        for word, weight in sorted_words:
            new_words.append(word)
        doc_map[doc] = new_words

    currDir = getcwd()
    chdir("searchapp/query_expan/")
    with open(out_file_name, 'w') as f:
        json.dump(doc_map, f, indent=2, sort_keys=True)
    chdir(currDir)
    
