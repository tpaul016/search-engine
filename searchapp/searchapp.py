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
    return jsonify(blah="blah")

@app.route('/spell', methods=['POST'])
def handleSpell():
    print(request.form)
    query = request.form["query"]
    dummyList = [query + " This", query + " is", query + " a", query + " test"]
    return jsonify(dummyList)
