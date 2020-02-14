from nltk.util import bigrams
from .. index_and_dict import indexAccess


def buildBiIndex(inverIndex):    
    biIndex = {}

    for token in inverIndex:
        bigramList = bigrams(token)
        bigramListLen = len(list(bigramList))
        breakpoint()
        for index, (firstChar, lastChar) in enumerate(bigramList):
            bigram = firstChar + lastChar

            # nltk's bigram generator does not create $m
            if index == 0:
                startBigram = "$" + firstChar
                if biIndex.get(startBigram):
                    biIndex[startBigram].append(token)
                else:
                    biIndex[startBigram] = [token]

            # nltk's bigram generator does not create m$
            elif index == bigramListLen - 1:
                endBigram = lastChar + "$" 
                if biIndex.get(endBigram):
                    biIndex[endBigram].append(token)
                else:
                    biIndex[endBigram] = [token]

            if biIndex.get(bigram):
                biIndex[bigram].append(token)
            else:
                biIndex[bigram] = [token]

    return biIndex
