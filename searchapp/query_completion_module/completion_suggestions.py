from searchapp.index_and_dict import indexAndDictBuilder, indexAccess
from searchapp.cor_access import corpus_enum

def get_suggestions(query, model, corpus, n_suggestions):
    formatted_query, ok = indexAndDictBuilder.preprocToken(query, stopword=True, stem=False, norm=True)
    if not ok:
        return []

    if corpus == corpus_enum.Corpus.COURSES:
        bigram_path = 'searchapp/bigram_language_model/courses_bigram_language_model.json'
    elif corpus == corpus_enum.Corpus.REUTERS:
        bigram_path = 'searchapp/bigram_language_model/reuters_bigram_language_model.json'

    bigram_model = indexAccess.get_bigram_index(bigram_path)

    try:
        suggestions = list(bigram_model[formatted_query]['conditional_words'].keys())[:n_suggestions]
    except:
        suggestions = []

    return suggestions
