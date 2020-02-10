import re

def hyphenRemoval(token):
    word = token.replace("-", "")

    # Don't want a word that's only hyphens
    if len(word) == 0:
        return(word, False)
    else:
        return(word, True)

    # Matches alphanumericString-alphanumericString
    #matches = re.findall('([a-zA-Z0-9]+)(-)([a-zA-Z0-9]+)', token)
    # matches will contain ['alphanumericString', '-' 'alphanumericString']
    #if len(matches) == 3:
    #    newWord = matches[0] + matches[1]
    #    return(newWord)
    #else:
    #    return(token)

def periodRemoval(token):
    word = token.replace(".", "")
    
    # Don't want a word that's only hyphens
    if len(word) == 0:
        return(word, False)
    else:
        return(word, True)

def normalize(token):
    newToken, ok = hyphenRemoval(token)
    if not ok:
        return newToken, False
    else:
        return newToken, True

    newToken, okPeriod = periodRemoval(token)
    if not ok:
        return newToken, False
    else:
        return newToken, True
