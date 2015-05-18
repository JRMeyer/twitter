# -*- coding: utf-8 -*-
# used to calculate relative frequency of hashtags
from __future__ import division
import sys
import codecs
import os
import pandas as pd
import matplotlib.pyplot as plt
import re
import csv
import ast
from nltk import FreqDist
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
                                     hashtag[0], (hashtag[1]/day[2]), hashtag[1]))
        # only look at n most common hashtags per day
        else:
            for hashtag in FreqDist(day[1]).items()[:numHashtags]:
                listOfTuples.append((pd.to_datetime(day[0], dayfirst=False), 
                                     hashtag[0], (hashtag[1]/day[2]), hashtag[1]))

    df = pd.DataFrame(listOfTuples,columns=['date', 'hashtag', 'freq', 'count'])

    print 'Hashtags read in...'
    print 'The shape of the DataFrame is: ' + str(df.shape)
    return df


def plot_common_hashtags(dirPath, lang, numHashtags, numHashtagsPlot):
    df = df_from_hashtags(dirPath, lang, numHashtags)

    # aggregate hashtags to find most common over all days
    groupDF = df.reset_index().groupby('hashtag').sum()
    sortedDF = groupDF['count'].order('count', ascending=False)

    plt.figure()
    sortedDF[:numHashtagsPlot].plot(kind='barh')
    plt.title('Most Common Hashtags')
    plt.show()



def plot_length_of_tweets(dirPath, lang, kind):
    '''
    create a histogram of length of tweets, in characters or tokens
    kind = 'char' or 'token'
    '''
    tweetLens=[]
    for tweetFile in os.listdir(dirPath):
        if os.path.isfile(dirPath+tweetFile):
            with open(dirPath+tweetFile, 'rU') as csvfile:
                rawFile = csv.reader(csvfile, delimiter='\t', quotechar='"')
                for rawTweet in rawFile:
                    text = codecs.decode(rawTweet[1], 'utf-8')
                    if rawTweet[4] == lang:
                        if kind == 'char':
                            tweetLens.append(len(text))
                        if kind == 'token':
                            tweetLens.append(len(text.split(' ')))
    print len(tweetLens)
    print np.mean(tweetLens)
    # use as many bins as longest tweet
    plt.hist(tweetLens, bins = max(tweetLens))
    # the 1.05* adds a little buffer space between edge of plot and max points
    xmax = (1.05*(max(tweetLens)))
    ymax = (1.05*(max([value for value in Counter(tweetLens).values()])))
    plt.axis([0, xmax, 0, ymax])
    plt.xlabel("Length")
    plt.ylabel("Frequency")
    plt.show()


def plot_token_count(dirPath, userORtweetLang, searchTerms):
    '''
    Given a search term, 'token', plot the percentage of tweets in which that
    token appears relative to all tweets in that language.
    '''
    if userORtweetLang == 'user':
        level = 4
    elif userORtweetLang == 'tweet':
        level = 5
    plt.figure()

    for lang in ['ru', 'uk', 'en']:
        dayTweetCounts=[]
        for tweetFile in os.listdir(dirPath):
            # make sure tweetFile is a file, not a dir
            if os.path.isfile(dirPath+tweetFile):
                numMatches = 0
                langTweets = 0
                totalTweets = 0
                with open(dirPath+tweetFile, 'rU') as csvfile:
                    rawFile = csv.reader(csvfile, delimiter='\t', quotechar='"')
                    for rawTweet in rawFile:
                        totalTweets+=1
                        if rawTweet[4] == lang:
                            langTweets+=1
                            date = rawTweet[3]
                            text = codecs.decode(rawTweet[1], 'utf-8').lower()
                            for token in searchTerms:
                                token = re.compile(token, re.UNICODE)
                                if re.search(token,text):
                                    numMatches+=1
                dayTweetCounts.append((pd.to_datetime(date, dayfirst=False),
                                       ((numMatches+1)/(langTweets+1))))
        df = pd.DataFrame(dayTweetCounts, columns=['date', 'freq'])
        df = df.sort('date', ascending=True)
        df[1:].plot(x='date', y='freq', label = lang)

    legend = plt.legend(loc='best')
    plt.title('Political Tweets per Day')
    plt.xlabel("Day")
    plt.ylabel("Percent of Tweets")
    plt.show()


def main():

    one = sys.argv[1]
    two = sys.argv[2]

    politics = 'политик|політик|politic'       # ru and en peak
    minsk = 'минск.*соглашен|мінськ.*угод|minsk agreement'   # lots higher and en peaks
    putin = 'путин|путін|putin'                # uk peaks early
    poroshenko = 'порошченко|poroshenko'       # low random 
    crimea = 'крым|крим|crimea'                # ukraine peaks early
    usa = 'обам[ау]|obama|сша|usa '                 # en peaks late
    war = 'войн[ау]|війн[ау]|war '             # peaks april
    news = 'новост|новини|news '                # 
    dnr = 'днр|dnr'                          # few
    lnr = 'лнр|lnr'                           # very few
    revolution = 'революци|революці|revolution' # very en peaks
    donbass = 'донбас|donbass'                 # uk peaks early
    donetsk = 'донецк|донецьк|donetsk'
    maidan = 'майдан|maidan'
    simferopol = 'севастополь|sevastopol'
    merged = [politics, minsk, putin, poroshenko, crimea, usa, news, dnr, lnr, 
              revolution, donbass, donetsk, maidan, war, simferopol]

    plot_token_count(one, two, merged)

    #plot_length_of_tweets(one, two, 'char')


if __name__ == "__main__":
    main()

