import json

def getInvertedIndex(path_to_index):
    # Read JSON content
    with open(path_to_index, 'r') as f:
        inverIndex = json.load(f)
    return inverIndex
