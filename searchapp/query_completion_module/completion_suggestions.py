from searchapp.index_and_dict import indexAndDictBuilder, indexAccess
from searchapp.cor_access import corpus_enum

def get_suggestions(query, model, corpus, n_suggestions):
    formatted_query, ok = indexAndDictBuilder.preprocToken(query, stopword=True, stem=False, norm=True)
    if not ok:
        return []

    bigram_model = indexAccess.get_bigram_model(corpus)

    try:
        suggestions = list(bigram_model[formatted_query]['conditional_words'].keys())[:n_suggestions]
    except:
        suggestions = []

    return suggestions
