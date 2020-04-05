import re
from nltk.corpus import wordnet as wn
from .. boolean_retrieval_model.query_pre_processing import query_to_postfix
from .. langproc import langProcess
from .. index_and_dict import indexAccess
from .. cor_access import corpus_enum


def expand_query(query, model, syn_amount, all_lemmas, corpus):
    """
        Generate a new query for specified model with expansions

        Args:
            syn_amount: amount of synonyms to use
            all_lemmas: the set of all synonyms
    """
    inverIndex, new_query, words = getIndexAndCleanQuery(model, corpus, query)

    used = []
    for word in words:
        # https://stackoverflow.com/questions/47932025/fastest-way-to-check-if-word-is-in-nltk-synsets
        if word in all_lemmas:
            synonyms = wn.synsets(word)[0].lemma_names()
            synonyms = synonyms[0:syn_amount]

            # TODO: Not sure if I should do this?
            # Remove words not in our index
            # filtered_syns = []
            # for syn in synonyms:
            #     if inverIndex.get(query):
            #         filtered_syns.append(syn)

            print("Global Expansion: word:", word, "syns:", synonyms)

            if len(synonyms) > 0:
                # Keep track of words used so we don't substitute the same word
                # twice
                if word not in used:
                    if model == "vsm":
                        new_query = new_query + " " + " ".join(synonyms)
                        used = used + synonyms
                    elif model == "boolean":
                        # Substitute in our expansion to where the word was
                        # origininally
                        sub = gen_replacement_bool(synonyms)
                        new_query = new_query.replace(word, sub)
                        used = used + synonyms
                    else:
                        print("glob_query: Invalid model!!!")
        else:
            print("Global Expansion: Dropped word", word)

    return new_query

def getIndexAndCleanQuery(model, corpus, query):
    if corpus is corpus_enum.Corpus.COURSES:
        file_name = 'courseIndex.json'
    elif corpus is corpus_enum.Corpus.REUTERS:
        file_name = 'reutersIndex.json'
    inverIndex = indexAccess.getInvertedIndex('searchapp/index_and_dict/' + file_name)

    if model == "vsm":
        words = clean_query_vsm(query)
        new_query = ''
    elif model == "boolean":
        words = clean_query_bool(query)
        new_query = query
    else:
        print("glob_query: Invalid model!!!")
    return inverIndex, new_query, words


def gen_replacement_bool(synonyms):
    """
        Generate string of synonyms concatenated with ORs
    """
    replacement = ""
    for syn in synonyms:
        if synonyms[len(synonyms) - 1] != syn:
            replacement = replacement + syn + " OR "
        else:
            replacement = replacement + syn
    return replacement


def clean_query_vsm(query):
    """
        Split words in query based on space
        TODO: Add more preprocessing? Casefolding, stemming
    """
    return query.split()


def clean_query_bool(query):
    """
        Strip out all the brackets, AND, OR and whitespace
    """
    words = re.split(r"\(|\)|AND|OR", query)
    cleaned_words = []
    for word in words:
        clean_w = word.strip()
        if clean_w != '':
            cleaned_words.append(clean_w)
    return cleaned_words
