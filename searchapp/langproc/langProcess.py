import re, string

def hyphenRemoval(token):
    token = re.sub(r'(-)', '', token)

    # Don't want a token that's only hyphens
    return(token)

def periodRemoval(token):
    token = re.sub(r'(\.)', '', token)
    return(token)

def generalPreProcess(token):
    # Remove all non-printable characters
    # https://stackoverflow.com/questions/8689795/how-can-i-remove-non-ascii-characters-but-leave-periods-and-spaces-using-python
    printable = set(string.printable)
    token = ''.join(filter(lambda x: x in printable, token))

    # Inspired from: https://stackoverflow.com/questions/46154561/remove-zero-width-space-unicode-character-from-python-string
    token = (token.encode('ascii', 'ignore')).decode('utf-8')

    # Remove all numbers
    token = re.sub(r'([0-9]+)', '', token)

    # Remove all forward slashes
    token = re.sub(r'(/)', '', token)

    # Remove all commas
    token = re.sub(r'(,)', '', token)

    # Remove all carets
    token = re.sub(r'(\^)', '', token)

    # Remove all percents
    token = re.sub(r'(%)', '', token)

    # Remove all Hashtags
    token = re.sub(r'(#)', '', token)

    # Remove all @ symbols
    token = re.sub(r'(@)', '', token)

    # Remove all * symbols
    token = re.sub(r'(\*)', '', token)

    # Remove all ? symbols
    token = re.sub(r'(\?)', '', token)

    # Remove all & symbols
    token = re.sub(r'(&)', '', token)
    
    # Remove all $ symbols
    token = re.sub(r'(\$)', '', token)

    # Remove all ~ symbols
    token = re.sub(r'(~)', '', token)

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
