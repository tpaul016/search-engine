from flask import Flask, render_template, jsonify, request
import nltk
import os
from .index_and_dict import indexAccess
from .index_and_dict import indexAndDictBuilder
from .cor_pre_proc import pre_processing
from .spelling_correction import spelling_correction

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

        print("Done creating app")

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
    print(docId)

    # Access Corpus and return a dictionary?

    # Mocking up with a nested dictionary 
    
    CSI9000 = {
        "docId": "CSI9000", 
        "title": "How do computers work", 
        "descr": "Blip bop boop I am a computer"
    }
    ADM123 = {
        "docId": "ADM123", 
        "title": "Crash course to Business", 
        "descr": "I have no idea, I've never taken a business course"
    }
    exampleCorpus = {}
    exampleCorpus["CSI9000"] = CSI9000
    exampleCorpus["ADM123"] = ADM123

    exampleDoc = exampleCorpus[docId]
    
    return render_template('document.html', docId=docId, title=exampleDoc["title"], descr=exampleDoc["descr"])

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
        {"docId": "CSI9000", "excerpt": "I am a link that works", "score": 9000},
        {"docId": "ADM123", "excerpt": "Learn to count to 2", "score": 2},
        {"docId": "CEG123", "excerpt": "Learn to count to 3", "score": 3},
        {"docId": "CHM123", "excerpt": "Learn to count to 4", "score": 4},
        {"docId": "MAT123", "excerpt": "Learn to count to 5", "score": 5},
        {"docId": "PHY123", "excerpt": "Learn to count to 6", "score": 6},
        {"docId": "MCG123", "excerpt": "Learn to count to 7", "score": 7},
        {"docId": "ELG123", "excerpt": "Learn to count to 8", "score": 8}
    ]
    return jsonify(exampleList)

@app.route('/spell', methods=['GET'])
def handleSpell():
    query = request.args.get('query')
    suggestions = spelling_correction.check_spelling(query, 10);
    print('spelling suggestions:')
    print(suggestions)
    return jsonify(suggestions)