from flask import Flask, render_template, jsonify, request
import nltk
import os
from .index_and_dict import indexAccess
from .index_and_dict import indexAndDictBuilder
from .cor_pre_proc import pre_processing
from .cor_access import corpusAccess

def create_app(test_config=None):
    # Perform corpus and index build for the first time
    if not (os.environ.get('FLASK_ENV') == 'development'):
        nltk.download('punkt') # Required for word tokenize 
        nltk.download('stopwords') # Required for stopword set 

        print("Creating app")
        # All these chdirs are required so files can be run as scripts or modules
        currDir = os.getcwd()
        os.chdir("searchapp/cor_pre_proc/")
        pre_processing.createCorpus()
        os.chdir(currDir)

        os.chdir("searchapp/cor_pre_proc/corpus")
        inverIndex = indexAndDictBuilder.buildIndex(True, True, True)
        os.chdir(currDir)

        os.chdir("searchapp/index_and_dict/")
        indexAndDictBuilder.serializeIndex(inverIndex)
        os.chdir(currDir)

    app = Flask(__name__)
    return app

app = create_app()

if app.config['DEBUG'] == True:
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docs/<docId>')
def getDocument(docId):
    document = corpusAccess.getDoc(docId)
    return render_template('document.html', docId=document["docId"], title=document["title"], descr=document["descr"])

@app.route('/docs', methods=['POST'])
def handleQuery():
    #index = indexAccess.getInvertedIndex()
    #breakpoint()

    print(request.form)
    query = request.form["query"]
    model = request.form["model"]
    collection = request.form["collection"]

    # Do stuff here and return a list of dictionaries?
    if model == "bool":
        x = 1 + 1 
        # ... pass in the collection to be used
    elif model == "vsm":
        x = 1 + 1
        # ... pass in the collection to be used

    # Mocking up with list of dictionaries
    exampleList = [
        {"docId": "CSI5168", "excerpt": "Learn to count to 1", "score": 9000},
        {"docId": "ADM2342", "excerpt": "Learn to count to 2", "score": 2},
        {"docId": "PSY6133", "excerpt": "Learn to count to 3", "score": 3},
    ]
    return jsonify(exampleList)

@app.route('/spell', methods=['POST'])
def handleSpell():
    print(request.form)
    query = request.form["query"]

    # Do stuff here and return a list of corrections?

    # Mocking up with list of corrections
    exampleList = [query + " This", query + " is", query + " a", query + " test"]
    return jsonify(exampleList)
