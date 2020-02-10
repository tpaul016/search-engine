
import json

def getInvertedIndex():
    # Read JSON content
    with open('searchapp/index_and_dict/index.json', 'r') as f:
        inverIndex = json.load(f)
    return inverIndex

    
