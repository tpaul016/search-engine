from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

if app.config['DEBUG'] == True:
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docs', methods=['POST'])
def handleQuery():
    print(request.form)
    query = request.form["query"]
    model = request.form["model"]
    collection = request.form["collection"]

    # Do stuff here and return a list of dictionaries?

    exampleList = [
        {"docId": "CSI123", "excerpt": "Learn to count to 1", "score": 1},
        {"docId": "ADM123", "excerpt": "Learn to count to 1", "score": 2},
        {"docId": "CEG123", "excerpt": "Learn to count to 1", "score": 3},
        {"docId": "CHM123", "excerpt": "Learn to count to 1", "score": 4},
        {"docId": "MAT123", "excerpt": "Learn to count to 1", "score": 5},
        {"docId": "PHY123", "excerpt": "Learn to count to 1", "score": 6},
        {"docId": "MCG123", "excerpt": "Learn to count to 1", "score": 7},
        {"docId": "ELG123", "excerpt": "Learn to count to 1", "score": 8}
    ]
    return jsonify(exampleList)

@app.route('/spell', methods=['POST'])
def handleSpell():
    print(request.form)
    query = request.form["query"]

    # Do stuff here and return a list of corrections?

    exampleList = [query + " This", query + " is", query + " a", query + " test"]
    return jsonify(exampleList)
