from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import nltk
from nltk.corpus import wordnet as wn
import os
from .index_and_dict import indexAndDictBuilder, biIndex
from .cor_pre_proc import pre_processing
from .cor_access import corpusAccess, corpus_enum
from .spelling_correction import spelling_correction
from .boolean_retrieval_model import query_pre_processing
from .boolean_retrieval_model import query_retrieval
from .query_expan import glob_query_expan
from .vsm import rank
from .relevance_feedback import relevance_index_access

def create_app(test_config=None):
    # Perform corpus and index build for the first time
    if not (os.environ.get('FLASK_ENV') == 'development'):
        nltk.download('punkt')  # Required for word tokenize
        nltk.download('stopwords')  # Required for stopword set
        nltk.download('wordnet')

        #print("Creating app ...")
        #pre_processing.createCourseCorpus("searchapp/cor_pre_proc/")

        # README: Change booleans here to toggle stopword, stemming and normalization respectively for Courses
        #inverIndex = indexAndDictBuilder.buildIndex(corpus_enum.Corpus.COURSES, True, True, True)
        #indexAndDictBuilder.serializeIndex("searchapp/index_and_dict/", inverIndex, "courseIndex.json")
        #biInd = biIndex.buildBiIndex(inverIndex)
        #indexAndDictBuilder.serializeIndex("searchapp/index_and_dict/", biInd, "courseBiIndex.json")

        # README: Change booleans here to toggle stopword, stemming and normalization respectively for Reuters
        #inverIndex = indexAndDictBuilder.buildIndex(corpus_enum.Corpus.REUTERS, True, True, True)
        #indexAndDictBuilder.serializeIndex("searchapp/index_and_dict/", inverIndex, "reutersIndex.json")
        #biInd = biIndex.buildBiIndex(inverIndex)
        #indexAndDictBuilder.serializeIndex("searchapp/index_and_dict/", biInd, "reutersBiIndex.json")

        #print("Done creating app")

    app = Flask(__name__)
    CORS(app)
    return app

app = create_app()

# https://stackoverflow.com/questions/47932025/fastest-way-to-check-if-word-is-in-nltk-synsets
all_lemmas = set(wn.all_lemma_names())

if app.config['DEBUG'] == True:
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/docs/<corpus>/<docId>')
def getDocument(corpus, docId):
    corpus_e = get_corpus_enum(corpus)
    document = corpusAccess.getDoc(docId, corpus_e)

    if corpus_e is corpus_enum.Corpus.COURSES:
        return render_template('document.html', docId=document["docId"], title=document["title"], descr=document["descr"])
    elif corpus_e is corpus_enum.Corpus.REUTERS:
        return render_template('document.html', docId=document["docId"], title=document["title"], descr=document["body"])
    else:
        return jsonify("Invalid corpus")


@app.route('/docs', methods=['POST'])
def handleQuery():

    query = request.form["query"]
    model = request.form["model"]
    collection = request.form["collection"]
    corpus = get_corpus_enum(collection)
    docs = []

    if collection == "courses":
        corpus = corpus_enum.Corpus.COURSES
    elif collection == "reuters":
        corpus = corpus_enum.Corpus.REUTERS
    else:
        print("No match for Corpus!!!!!")

    if model == "boolean":
        formatted_query = query_pre_processing.get_query_documents(query, corpus)
        docs = query_retrieval.execute_query(formatted_query)
        print("--------------------------------")
        print("Boolean")
        print("--------------------------------")
    elif model == "vsm":
        docs = rank.rank(query, collection, corpus)
        print("--------------------------------")
        print("VSM")
        print("--------------------------------")
    expan_query = glob_query_expan.expand_query(query, model, 3, all_lemmas, corpus)
    result = {"docs": docs, "expans": expan_query}
    print("Global Expansion: Expanded Query", expan_query)
    
    return jsonify(result)

def get_corpus_enum(corpus_string):
    if corpus_string == "courses":
        return corpus_enum.Corpus.COURSES
    elif corpus_string == "reuters":
        return corpus_enum.Corpus.REUTERS
    else:
        print("No match for Corpus!!!!!")
        return "No match for Corpus!!!"


@app.route('/spell', methods=['GET'])
def handleSpell():
    query = request.args.get('query')
    model = request.args.get('model')
    collection = request.args.get('corpus')
    corpus = get_corpus_enum(collection)

    suggestions = spelling_correction.check_spelling(query, 10, model, corpus)
    print('spelling suggestions:')
    print(suggestions)
    return jsonify(suggestions)


@app.route('/relevance', methods=['PUT'])
def handleRelevance():
    query = request.args.get('query')
    docId = request.args.get('docId')
    type = request.args.get('type')
    checked = request.args.get('checked') == "true"
    print(query)

    relevance_index_access.update(query, docId, type, checked)
    return jsonify('updated')

