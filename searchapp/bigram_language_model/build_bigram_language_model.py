from os import listdir
from os.path import join
from bs4 import BeautifulSoup
import nltk
from searchapp.cor_access import corpus_enum
from searchapp.index_and_dict import indexAndDictBuilder
import json

def process_tokens(tokens, stopword, stem, norm):
    processed_tokens = []
    for token in tokens:
        token, ok = indexAndDictBuilder.preprocToken(token, stopword, stem, norm)
        if not ok:
            continue
        processed_tokens.append(token)
    return processed_tokens

def build_bigram_language_module(corpus, stopword, stem, norm):
    print ('Building Bigram Language Model ...')

    bigram_language_model = {}
    # path = "searchapp/cor_pre_proc/" + corpus.value
    path = "../cor_pre_proc/" + corpus.value
    files = [join(path, f) for f in listdir(path)]

    for f_path in files:
        with open(f_path) as f:
            soup = BeautifulSoup(f, "xml")

        if corpus == corpus_enum.Corpus.COURSES:
            desc = soup.desc.string
        elif corpus == corpus_enum.Corpus.REUTERS:
            desc = soup.body.string

        if desc is not None:
            tokens = nltk.word_tokenize(desc)
            tokens = process_tokens(tokens, stopword, stem, norm)
            for i in range(len(tokens)-1):
                token = tokens[i]
                if token not in bigram_language_model:
                    bigram_language_model[token] = {
                        'tf': 0,
                        'conditional_words': {}
                    }

                bigram_language_model[token]['tf'] += 1
                next_token = tokens[i+1]
                if next_token not in bigram_language_model[token]['conditional_words']:
                    bigram_language_model[token]['conditional_words'][next_token] = 1
                else:
                    bigram_language_model[token]['conditional_words'][next_token] += 1

    for token in bigram_language_model:
        bigram_language_model[token]['conditional_words'] = dict(sorted(bigram_language_model[token]['conditional_words'].items(), key=lambda x: x[1], reverse=True))

    with open('./bigram_language_model.json', 'w') as file:
        json.dump(bigram_language_model, file, indent=2)

build_bigram_language_module(corpus_enum.Corpus.REUTERS, True, False, True)
