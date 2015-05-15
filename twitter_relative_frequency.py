# -*- coding: utf-8 -*-
from __future__ import division
import sys
import codecs
import os
from nltk import FreqDist
# Chris Potts' regex
from twitter_regex import *
from scipy import log


def tokenize(tweetText):
    '''
    Takes any string or unicode object (tweet) and
    returns a tokenized list of strings (words).
    '''
    # strip the first and last double quote off tweet
    tweet = tweetText[1:-1]
    goodWords=[]
    # tokenize using the word_re regex from twitter_regex
    words = word_re.findall(tweet)
    # make all tokens lowercase except emoticons
    words = map((lambda x : x if emoticon_re.search(x) else x.lower()), words)
    for word in words:
        # throw out all the mentions (@'s) and URLs
        if (re.compile('^@').search(word) or re.compile('^http').search(word)):
            pass
        else:
            goodWords.append(word)
    return goodWords


def docTF_over_corpusTF(dirPath, lang, searchTerm):
    '''
    Returns a dictionary with tokens as keys and relative frequencies as values.
    Given a search term, 'token', the function groups all tweets with that token
    together to form a document. Then it returns the log of the frequency of 
    tokens in that document over frequency of those tokens outside the document.
    The logic is meant to be similar to tf-idf.
    '''
    searchTerm = codecs.decode(searchTerm, 'utf-8')
    docTokens=[]
    corpusTokens=[]
    for tweetFile in os.listdir(dirPath):
        # make sure tweetFile is a file, not a dir
        if os.path.isfile(dirPath+tweetFile):
            # using codecs for encoding issues, not sure if needed
            rawFile = codecs.open(dirPath + tweetFile, 'r', 'utf-8')
            # my tweet files have one tweet per line
            for rawTweet in rawFile:
                try:
                    # just look at one language
                    if rawTweet.split('\t')[4] == lang:
                        tweetText = rawTweet.split('\t')[1].lower()
                        tokens = tokenize(tweetText)
                        # look for the search term in the tweet text
                        if re.compile(searchTerm).search(tweetText):
                            docTokens.append(tokens)
                        else:
                            corpusTokens.append(tokens)
                # issues with windows ^M newline
                except:
                    pass

    # make lists of vocab for each set
    docVocab = [token for doc in docTokens for token in doc]
    corpusVocab = [token for doc in corpusTokens for token in doc]

    # make frequency distributions with nltk, excluding hapaxes from document
    docFD = {key:value for key,value in FreqDist(docVocab).items() if value > 1}
    corpusFD = FreqDist(corpusVocab)

    # calculate relative frequency for each token
    docOverCorpusTF={}
    for key in docFD.keys():
        if key in corpusFD.keys():
            docOverCorpusTF[key] = log(docFD[key]/corpusFD[key])
        else:
            docOverCorpusTF[key] = log(docFD[key]/1)

    f = codecs.open('results.txt', 'w', 'utf-8')
    f.write(str(len(docTokens)) + 
            " tweets were found *with* the search term: " + searchTerm +"\n")
    f.write(str(len(corpusTokens)) + 
            " tweets were found *without* the search term: " + searchTerm +"\n")
    for item in sorted(docOverCorpusTF, key=docOverCorpusTF.get):
        f.write("%s\n" % item)
    f.close()
            

def main():
    dirPath = sys.argv[1]
    lang = sys.argv[2]
    politics = 'политик|політик|politic'
    minsk = 'минск|мінськ|minsk'
    putin = 'путин|путін|putin'
    poroshenko = 'порошченко|poroshenko'
    crimea = 'крым|crimea'
    usa = 'обам|obama|сша|usa'
    war = 'войн|війн|war'
    news = 'новост|новини|news'

    docTF_over_corpusTF(dirPath, lang, poroshenko)


if __name__ == "__main__":
    main()
