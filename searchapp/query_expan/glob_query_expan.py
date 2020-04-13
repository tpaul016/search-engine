import re
from nltk.corpus import wordnet as wn
from .. boolean_retrieval_model.query_pre_processing import query_to_postfix
from .. langproc import langProcess
from .. index_and_dict import indexAccess
from .. cor_access import corpus_enum


def expand_query(query, model, senses, all_lemmas, corpus, syn_weight):
    print("Global Expansion: Input:", query)
    """
        Generate a new query for specified model with expansions

        Args:
            senses: The amount of synsets or meanings to use
            all_lemmas: the set of all synonyms
            syn_weight: Integer weight a synonym should have.
    """
    inverIndex, new_query, words = getIndexAndCleanQuery(model, corpus, query)

    used = []
    for word in words:
        # https://stackoverflow.com/questions/47932025/fastest-way-to-check-if-word-is-in-nltk-synsets
        if word in all_lemmas:
            synonyms = get_synonyms(word, senses, inverIndex)

            print("Global Expansion: word:", word, "syns:", synonyms)

            if len(synonyms) > 0:
                if model == "vsm":
                    new_query += gen_query_vsm(word, synonyms, syn_weight)
                elif model == "boolean":
                    # Substitute in our expansion to where the word was
                    # origininally
                    print(word)
                    sub = gen_replacement_bool(word, synonyms)
                    #Inspired from https://stackoverflow.com/questions/17730788/search-and-replace-with-whole-word-only-option
                    new_query = re.sub(r"\b%s\b" % word, sub, new_query)
                else:
                    print("glob_query: Invalid model!!!")
        else:
            print("Global Expansion: Word not in index ", word)

    return new_query


def get_synonyms(word, senses, inverIndex):
    synsets = wn.synsets(word)
    synonyms = []

    for i, syns in enumerate(synsets):
        if i >= senses:
            break
        synonyms += syns.lemma_names()

    # Remove words not in our index
    synonyms = remove_words_not_in_index(word, synonyms, inverIndex)
    synonyms = synonyms[0:5]
    return synonyms


def remove_words_not_in_index(word, synonyms, inverIndex):
    filt_syns = []
    if len(synonyms) == 1:
        return [word]

    for syn in synonyms:
        if syn != word:
            if inverIndex.get(langProcess.stem(syn)):
                filt_syns.append(syn)
            #else:
            #    print("Global Expansion: Dropped synonym:", syn)

    if len(filt_syns) == 0:
        return [word]

    return filt_syns


def gen_query_vsm(word, synonyms, syn_weight):
    addition = word + " (1) "
    for syn in synonyms:
        if syn == word:
            continue
        addition += syn + " (" + str(syn_weight) + ") "

    return addition


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


def gen_replacement_bool(word, synonyms):
    """
        Generate string of synonyms concatenated with ORs
    """
    if len(synonyms) == 0 or (synonyms[0] == word and len(synonyms) == 1):
        return word

    replacement = "(" + word + " OR " + synonyms[0] + ")"
    added = [synonyms[0]]
    for i, syn in enumerate(synonyms):
        # We've already added the first synonym
        if i == 0:
            continue
        if syn not in added:
            replacement = "(" + replacement + " OR " + syn + ")"
            added.append(syn)
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
