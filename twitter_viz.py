# -*- coding: utf-8 -*-
# used to calculate relative frequency of hashtags
from __future__ import division
import sys
import codecs
import os
import pandas as pd
import matplotlib.pyplot as plt
import re

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
            # using codecs for encoding issues, not sure if needed
            rawFile = codecs.open(dirPath + tweetFile, 'r', 'utf-8')
            # my tweet files have one tweet per line
            for rawTweet in rawFile:
                try:
                    date = rawTweet.split('\t')[3]
                    # just look at one language
                    if rawTweet.split('\t')[4] == lang:
                        numTweets += 1
                        # hashtags in as third column of file
                        hashtag = ast.literal_eval(rawTweet.split('\t')[2])
                        # if the list 'hashtag' has contents
                        if hashtag:
                            # each hashtag is an entry in a dict
                            for d in hashtag:
                                oneDay.append([d['text']][0].lower())
                # ^M (Windows newline) keeps goofing things up
                except:
                    pass
        hashList.append((date, oneDay, numTweets))
    listOfTuples=[]
    for day in hashList:
        # only look at n most common hashtags per day
        for hashtag in FreqDist(day[1]).items()[:numHashtags]:
            listOfTuples.append((pd.to_datetime(day[0], dayfirst=False), 
                                 hashtag[0], (hashtag[1]/day[2]), hashtag[1]))
    df = pd.DataFrame(listOfTuples, 
                      columns=['date', 'hashtag', 'freq', 'count'])
    print 'Hashtags read in...'
    return df 



def plot_common_hashtags(dirPath, lang, numHashtags, numHashtagsPlot):
    df = df_from_hashtags(dirPath, lang, numHashtags)
    print df[df['hashtag']==u'україна']

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
        # make sure tweetFile is a file, not a dir
        if os.path.isfile(dirPath+tweetFile):
            # using codecs for encoding issues, not sure if needed
            rawFile = codecs.open(dirPath + tweetFile, 'r', 'utf-8')
            # my tweet files have one tweet per line
            for rawTweet in rawFile:
                try:
                    # just look at one language
                    if rawTweet.split('\t')[4] == lang:
                        if kind == 'char':
                            tweetLens.append(len(rawTweet.split('\t')[1]))
                        if kind == 'token':
                            tweetLens.append(len(
                                rawTweet.split('\t')[1].split(' ')))
                except:
                    pass
    plt.hist(tweetLens, bins=35)
    plt.axis([0, 35, 0, 80000])
    plt.title("Russian Tweet Length Histogram")
    plt.xlabel("Length")
    plt.ylabel("Frequency")
    plt.show()


def plot_token_count(dirPath, token):
    '''
    Given a search term, 'token', plot the percentage of tweets in which that
    token appears relative to all tweets in that language.
    '''
    plt.figure()
    token = codecs.decode(token, 'utf-8')
    for lang in ['ru', 'uk', 'en']:
        dayTweetCounts=[]
        for tweetFile in os.listdir(dirPath):
            print tweetFile
            numTokens = 0
            numTweets = 0
            # make sure tweetFile is a file, not a dir
            if os.path.isfile(dirPath+tweetFile):
                # using codecs for encoding issues, not sure if needed
                rawFile = codecs.open(dirPath + tweetFile, 'r', 'utf-8')
                # my tweet files have one tweet per line
                for rawTweet in rawFile:
                    try:
                        date = rawTweet.split('\t')[3]
                        # just look at one language
                        if rawTweet.split('\t')[4] == lang:
                            numTweets+=1
                            # look for the search term in the tweet text
                            if re.compile(token).search(rawTweet.split('\t')[1].lower()):
                                numTokens+=1
                    except:
                        pass
            dayTweetCounts.append((pd.to_datetime(date, dayfirst=False), 
                                   numTokens/(numTweets+1)))
        df = pd.DataFrame(dayTweetCounts, columns=['date', 'freq'])
        df = df.sort('date', ascending=True)
        df[1:].plot(x='date', y='freq', label = lang)

    legend = plt.legend(loc='best')
    plt.title('Frequency of Matches per Day for Political Terms')
    plt.show()


def main():
    dirPath = sys.argv[1]

    merged = 'минск|мінськ|minsk|путин|путін|putin|порошченко|poroshenko|крым|crimea|обам|obama|сша|usa|війн|war|новост|новини|news'
    politics = 'политик|політик|politic'
    minsk = 'минск|мінськ|minsk'
    putin = 'путин|путін|putin'
    poroshenko = 'порошченко|poroshenko'
    crimea = 'крым|crimea'
    usa = 'обам|obama|сша|usa'
    war = 'войн|війн|war'
    news = 'новост|новини|news'

    plot_token_count(dirPath,merged)


if __name__ == "__main__":
    main()
