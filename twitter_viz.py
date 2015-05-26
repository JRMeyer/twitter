# -*- coding: utf-8 -*-
from __future__ import division
from twitter_helpers import DataFrame_from_tweets
import sys
import codecs
import os
import pandas as pd
import matplotlib.pyplot as plt
import re
import csv
import ast
# from nltk import FreqDist
from collections import Counter
import numpy as np
import csv


def df_from_hashtags(dirPath, lang, numHashtags):
    '''
    returns a pandas DataFrame with one row per date + hashtag and four colums:
    (0) date (1) the hashtag (2) n occurances of hashtag/n total tweets in file
    (3) n total occurances of hashtag

    dirPath = dir containing tweet files
    lang = langauge
    numHashtags = number of top hashtags per day
    '''
    hashList=[]
    for tweetFile in os.listdir(dirPath):
        # make sure tweetFile is file, not a dir
        if os.path.isfile(dirPath+tweetFile):
            numTweets=0
            oneDay=[]
            with open(dirPath+tweetFile, 'rU') as csvfile:
                rawFile = csv.reader(csvfile, delimiter='\t', quotechar='"')
                for rawTweet in rawFile:
                    date = rawTweet[3]
                    # just look at one language
                    if rawTweet[4] == lang:
                        numTweets += 1
                        hashtag = ast.literal_eval(rawTweet[2])
                        # if the list 'hashtag' has contents
                        if hashtag:
                            # each hashtag is an entry in a dict
                            for d in hashtag:
                                oneDay.append([d['text']][0].lower())
        hashList.append((date, oneDay, numTweets))
        
    listOfTuples=[]
    for day in hashList:
        if numHashtags == 'all':
            for hashtag in FreqDist(day[1]).items():
                listOfTuples.append((pd.to_datetime(day[0], dayfirst=False), 
                                     hashtag[0], (hashtag[1]/day[2]),
                                     hashtag[1]))
        # only look at n most common hashtags per day
        else:
            for hashtag in FreqDist(day[1]).items()[:numHashtags]:
                listOfTuples.append((pd.to_datetime(day[0], dayfirst=False), 
                                     hashtag[0], (hashtag[1]/day[2]),
                                     hashtag[1]))

    df = pd.DataFrame(listOfTuples,columns=['date', 'hashtag', 'freq', 'count'])

    print 'Hashtags read in...'
    print 'The shape of the DataFrame is: ' + str(df.shape)
    return df


def plot_common_hashtags(myPath, lang, numHashtags, numHashtagsPlot):
    df = df_from_hashtags(myPath, lang, numHashtags)

    # aggregate hashtags to find most common over all days
    groupDF = df.reset_index().groupby('hashtag').sum()
    sortedDF = groupDF['count'].order('count', ascending=False)

    plt.figure()
    sortedDF[:numHashtagsPlot].plot(kind='barh')
    plt.title('Most Common Hashtags')
    plt.show()


def plot_length_of_tweets(myPath, kind):
    '''
    INPUT:
    myPath = a dir or file path
    kind = 'char' or 'token'
    OUTPUT:
    a histogram of length of tweets, in characters or tokens
    '''
    df = DataFrame_from_tweets(myPath)

    tweetLens = []
    tweetTexts = df['text']
    for tweetText in tweetTexts:
        text = codecs.decode(tweetText, 'utf-8')
        if kind == 'char':
            tweetLens.append(len(text))
        if kind == 'token':
            tweetLens.append(len(text.split(' ')))
                
    # use as many bins as longest tweet
    plt.hist(tweetLens, bins = max(tweetLens))
    # the 1.05* adds a little buffer space between edge of plot and max points
    xmax = (1.05*(max(tweetLens)))
    ymax = (1.05*(max([value for value in Counter(tweetLens).values()])))
    plt.axis([0, xmax, 0, ymax])
    plt.xlabel("Length")
    plt.ylabel("Frequency")
    plt.show()


def plot_regex_matches(myPath, searchTerms, level='tweet_lang'):
    '''
    INPUT:
    (1) a list of unicode search terms
    (2) a directory
    (3) either 'user_lang' or 'tweet_lang'
    OUTPUT:
    (1) longitudinal linegraph of percentage of tweets which match that regex
    for each language
    '''
    # read in all tweets as DataFrame
    df = DataFrame_from_tweets(myPath)
    # initialize empty DataFrame to store daily counts
    combinedDF = pd.DataFrame()

    # compile our search terms as regex
    regex = (u'|').join(searchTerms)
    
    for lang in ['ru', 'uk', 'en']:
        # subset just tweets from one language
        langDF = df[df.loc[:,(level)]==lang]
        langDF.loc[:,('date')] = langDF.loc[:,('time')].apply(lambda x:
                                        pd.to_datetime(x, dayfirst=True).date())
        langTotal = langDF.date.value_counts()

        # subset tweets containing regex
        langMatches = langDF[langDF.text.str.contains(regex,flags=re.IGNORECASE,
                                                regex=True)].date.value_counts()
        
        freqDF = pd.concat([langMatches, langTotal], axis=1)
        # plus-1 smoothing numerator
        freqDF = freqDF.fillna(1)
        # plus-1 smoothing denominator and freq calculation
        freqSeries = freqDF.apply(lambda row: (row[0]/(row[1]+1))*100,
                                        axis=1)

        combinedDF[lang] = freqSeries

    combinedDF.plot()
    plt.legend(loc='best')
    plt.title('Political Tweets per Day')
    plt.xlabel("Day")
    plt.ylabel("Percent of Tweets")
    plt.show()

    

def main():

    myPath= sys.argv[1]
    kind = sys.argv[2]

    politics = u'политик|політик|politic'
    minsk = u'минск.*соглашен|мінськ.*угод|minsk agreement'
    putin = u'путин|путін|putin'
    poroshenko = u'порошченко|poroshenko' 
    crimea = u'крым|крим|crimea'
    usa = u'обам[ауео]|obama|сша|usa '
    war = u'войн[ауео]|війн[ауео]|war '
    news = u'новост|новини|news '
    dnr = u'днр|dnr'
    lnr = u'лнр|lnr'
    revolution = u'революци|революці|revolution'
    donbass = u'донбас|donbass'
    donetsk = u'донецк|донецьк|donetsk'
    maidan = u'майдан|maidan'
    simferopol = u'севастополь|sevastopol'
    merged = [politics, minsk, putin, poroshenko, crimea, usa, news, dnr, lnr,
              revolution, donbass, donetsk, maidan, war, simferopol]

    plot_length_of_tweets(myPath, kind)


if __name__ == "__main__":
    main()

