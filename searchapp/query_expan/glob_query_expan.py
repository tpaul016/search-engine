import re
from nltk.corpus import wordnet as wn
from .. boolean_retrieval_model.query_pre_processing import query_to_postfix
from .. langproc import langProcess


def expand_query(query, model, syn_amount, all_lemmas):
    """
        Generate a new query for specified model with expansions

        Args:
            syn_amount: amount of synonyms to use
            all_lemmas: the set of all synonyms
    """
    if model == "vsm":
        words = clean_query_vsm(query)
        new_query = ''
    elif model == "boolean":
        words = clean_query_bool(query)
        new_query = query
    else:
        print("glob_query: Invalid model!!!")

    used = []
    for word in words:
        # https://stackoverflow.com/questions/47932025/fastest-way-to-check-if-word-is-in-nltk-synsets
        if word in all_lemmas:
            synonyms = wn.synsets(word)[0].lemma_names()
            synonyms = synonyms[0:syn_amount]
            print("Global Expansion: word:", word, "syns:", synonyms)
            if len(synonyms) > 0:
                if model == "vsm":
                    if word not in used:
                        new_query = new_query + " " + " ".join(synonyms)
                        used = used + synonyms
                elif model == "boolean":
                    # Keep track of words used so we don't substitute the same word
                    # twice
                    if word not in used:
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








