from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
def index():
    query = ''
    model = ''
    collection = ''
    return render_template('index.html', query=query)

@app.route('/docs/docId')
def get_document(docId):
    return docId

