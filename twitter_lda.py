# -*- coding: utf-8 -*-
'''
This script contains a main run_lda() function in addition to others.
The other functions are mostly for visualization.

USAGE:
$ python twitter_lda.py '/home/fetched_tweets/' u':(' 'ru'

The three sys.argv arguments are: 
(1) path to dir containing twitter files
(2) the key term you want to subset the data set by
(3) the language (two letter code) you want to use
'''

# used to calculate relative frequency of hashtags
from __future__ import division
# Chris Potts' regex
from twitter_regex import *
import sys
# evaluate a string as code
import ast
import numpy as np
import lda 
import os
import re
# for encoding
import codecs
from nltk import FreqDist
from nltk.stem import SnowballStemmer
from scipy.sparse import lil_matrix
import time
from scipy import log



def main():
    dirPath = sys.argv[1]
    keyTerm = 'минск|м.нськ|minsk|путин|putin|порошченко|poroshenko|крым|crimea|обам|obama|сша|usa|в.йн|war'
    run_lda(dirPath,
            keyTerm,
            lang = 'ru',
            docKind = 'tweet',
            outFile = 'results.txt',
            # throw out tweets not longer than this
            tweetLenCutOff = 5,
            # throw out words occuring less than this many times
            wordBottomCutOff = 5,
            # Ramage et al throws out top 30 words
            wordTopCutOff = 30,
            n_topics = 100,
            n_iter = 1500,
            random_state = 1,
            n_top_words = 8,
            stemming = False)


def tokenize_tweets(dirPath, lang, tweetLenCutOff, keyTerm):
    '''
    returns a list of tokenized tweets
    '''
    tokenizedTweets=[]
    for tweetFile in os.listdir(dirPath):
        print tweetFile
        # make sure tweetFile is a file, not a dir
        if os.path.isfile(dirPath+tweetFile):
            # using codecs for encoding issues, not sure if needed
            rawFile = codecs.open(dirPath + tweetFile, 'r', 'utf-8')
            # my tweet files have one tweet per line
            for rawTweet in rawFile:
                try:
                    # just look at one language
                    if rawTweet.split('\t')[4] == lang:
                        # my tab-delimited tweet file has text as second col
                        text = rawTweet.split('\t')[1]
                        if re.compile(keyTerm).search(text.lower()):
                            # tokenize tweet
                            tokens = tokenize(text)
                            # append tweets with n or more words (Zhao 2011)
                            if len(tokens) > tweetLenCutOff:
                                tokenizedTweets.append(tokens)
                # ^M (Windows newline) keeps goofing things up
                except:
                    pass
    print str(len(tokenizedTweets)) + " tweets were found matching the keyterm"
    return tokenizedTweets


def make_hashtag_dict(dirPath, lang):
    '''
    returns a dictionary with hashtags as keys and empty lists as entries
    '''
    docDict={}
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
                        # hashtags in as third column of file
                        hashtag = ast.literal_eval(rawTweet.split('\t')[2])
                        # if the list has contents
                        if hashtag:
                            # the hashtags are stored as entries in a dict
                            for d in hashtag:
                                # and 'text' is the key
                                docDict[d['text']]=[]
                # ^M (Windows newline) keeps goofing things up
                except:
                    pass
    print 'Hashtag dictionary made...'
    return docDict


def make_new_docs(tokenizedTweets, docDict):
    '''
    every tweet with a hashtag gets appended to that hashtag's entry in docDict
    '''
    for tweet in tokenizedTweets:
        for token in tweet:
            if token in docDict:
                docDict[token].append(tweet)
            elif '#' in token:
                if token[1:] in docDict:
                    docDict[token[1:]].append(tweet)
    print 'Tweets grouped by hashtags...'
    return docDict


def flatten_subLists(superList):
    newList=[]
    for subList in superList:
        newSubList=[]
        for subSubList in subList:
            for item in subSubList:
                newSubList.append(item)
        newList.append(newSubList)
    print 'Sublists flattened...'
    return newList


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


def make_cutOff(flatList, bottomCutOff, topCutOff):
    '''
    INPUT:
    flatList is a 1-d list of all tokens in set of tweets and both bottom and
    topCutOff are intergers
    OUTPUT:
    newVocab = a 1-d list of all tokens we want to keep
    thrownOut = a 1-d list of all tokens to throw out
    '''
    fd = FreqDist(flatList)
    newVocab = []
    thrownOut = []
    
    for item in fd.items()[:topCutOff]:
        # append most common words
        thrownOut.append(item)

    for item in fd.items()[topCutOff:]:
        if item[1] > bottomCutOff:
            # append good words
            newVocab.append(item[0])
        else:
            # append uncommon words
            thrownOut.append(item)

    print 'Cutoffs made...'
    return newVocab, thrownOut


def make_X(tweetList,featDict):
    ''' 
    tweetList is a list of tokenized tweets
    featDict is a dictionary of feature:index pairs (feature is a token)
    '''
    # number of rows
    numTweets = len(tweetList)
    # number of columns
    numFeats = len(featDict)
    # make empty matrix with shape (rows, cols)
    X = lil_matrix((numTweets, numFeats))

    row = 0
    for tweet in tweetList:
        for token in tweet:
            if token in featDict:
                # the value to a key (token) is the column number
                X[row,featDict[token]] += 1
        row += 1
    print 'X-matrix made with shape: ' + str(X.shape) + '...'
    return X


def stem_words(docs, stemmer):
    newDocs=[]
    for doc in docs:
        newDoc=[]
        for token in doc:
            newDoc.append(stemmer.stem(token))
        newDocs.append(newDoc)
    print 'Words stemmed...'
    return newDocs


def print_results_to_file(model, vocab, n_top_words, shapeX, lang, keyTerm,
                          tweetLenCutOff, wordBottomCutOff, wordTopCutOff, 
                          n_topics, n_iter, docKind, stemmer, outFile):

    # model.components_ also works
    topic_word = model.topic_word_
    numRows, numCols = shapeX
    f = codecs.open(outFile, 'w', 'utf-8')
    f.write('LDA was run on ' + str(numRows) + ' separate documents\n')
    f.write('There were a total of ' + str(numCols) + ' features used\n')
    f.write('The language of tweet was ' + lang + '\n')
    f.write('The keyTerm was ' + keyTerm + '\n')
    f.write('All tweets were at least ' + str(tweetLenCutOff) 
            + ' tokens long\n')
    f.write('Tokens occuring less than ' + str(wordBottomCutOff) 
            + ' times were discarded\n')
    f.write('The ' + str(wordTopCutOff) 
            + ' most frequent tokens were discarded\n')
    f.write('There were ' + str(n_topics) + ' topics discovered\n')
    f.write('There were ' + str(n_iter) + ' iterations\n')
    f.write('The documents were grouped at the ' + docKind + ' level\n')
    if stemmer == None:
        f.write('No stemmer was used\n')
    else:
        f.write('A stemmer was used\n')

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        for word in topic_words:
            f.write("%s\n" % word)
        f.write("=============\n")
    f.close()


def run_lda(dirPath, keyTerm, lang, docKind, outFile, tweetLenCutOff,
            wordBottomCutOff, wordTopCutOff, n_topics, n_iter, random_state,
            n_top_words, stemming):

    start = time.time()

    keyTerm = codecs.decode(keyTerm, 'utf-8')

    # return a list of tokenized tweets and a dictionary with hashtags as keys
    tokenizedTweets = tokenize_tweets(dirPath, lang, tweetLenCutOff, keyTerm)
                                                       
    # set docs as either individual tweets or grouped by hashtags
    if docKind == 'hash':
        emptyDict = make_hashtag_dict(dirPath, lang)
        docDict = make_new_docs(tokenizedTweets, emptyDict)
        docs = flatten_subLists(docDict.values())
    elif docKind == 'tweet':
        docs = tokenizedTweets
    
    # discard empty docs
    docs = [doc for doc in docs if doc]

    # stem tokens or don't
    if stemming == True:
        if lang == 'ru':
            stemmer = SnowballStemmer('russian')
            docs = stem_words(docs, stemmer)
    elif stemming == False:
        stemmer = None
        pass

    # make 1-dimensional list of tokens
    vocab = [token for doc in docs for token in doc]

    # cutoffs for common and rare tokens
    newVocab, thrownOut = make_cutOff(vocab, wordBottomCutOff, wordTopCutOff)

    # create feature dictionary with token as key and column index as value
    featDict = {token:index for index, token in enumerate(set(newVocab))}
                
    # create X matrix
    X = make_X(docs,featDict)

    # run the LDA
    model = lda.LDA(n_topics, n_iter, random_state)
    model.fit(X)

    # print results
    shapeX = X.shape
    print_results_to_file(model, newVocab, n_top_words, shapeX, lang, keyTerm,
                          tweetLenCutOff, wordBottomCutOff, wordTopCutOff, 
                          n_topics, n_iter, docKind, stemmer, outFile)
    end = time.time()
    print end - start


if __name__ == "__main__":
    main()



