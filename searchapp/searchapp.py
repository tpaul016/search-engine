from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


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
def handleQSpell():
    print(request.form)
    query = request.form["query"]
    return jsonify(blip="blop")
