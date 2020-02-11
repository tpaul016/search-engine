import re

def hyphenRemoval(token):
    token = re.sub(r'(-)', '', token)

    # Don't want a token that's only hyphens
    return(token)

def periodRemoval(token):
    token = re.sub(r'(\.)', '', token)
    return(token)

def generalPreProcess(token):
    # Remove all numbers
    token = re.sub(r'([0-9]+)', '', token)

    # Remove all forward slashes
    token = re.sub(r'(/)', '', token)

    # Remove unicode characters
    # Inspired from: https://stackoverflow.com/questions/46154561/remove-zero-width-space-unicode-character-from-python-string
    token = (token.encode('ascii', 'ignore')).decode('utf-8')

    # Remove appostrophes 
    token = re.sub(r'(\')', '', token)

    # Remove plus signs 
    token = re.sub(r'(\+)', '', token)

    # Case fold to lower case
    token = token.lower()
    return token

def normalize(token):
    token = hyphenRemoval(token)
    token = periodRemoval(token)
    return token
