from flask import Flask, render_template, jsonify, request
from .dictbuild import dictBuilder
import nltk
app = Flask(__name__)

if app.config['DEBUG'] == True:
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Necessary for word_tokenize()
nltk.download('punkt')

# Build Dictionary
dictBuilder.buildDict(True, True, True)

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

@app.route('/spell', methods=['POST'])
def handleSpell():
    print(request.form)
    query = request.form["query"]

    # Do stuff here and return a list of corrections?

    # Mocking up with list of corrections
    exampleList = [query + " This", query + " is", query + " a", query + " test"]
    return jsonify(exampleList)
