# -*- coding: utf-8 -*-
from __future__ import division
from twitter_helpers import DataFrame_from_tweets
import sys
import codecs
import os
import re
import ast
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter



def plot_common_hashtags(myPath, kind='tweet_lang', numHashtags=10):
    '''
    INPUT:
    (1) a directory of files
    (2) either 'user_lang' or 'tweet_lang'
    OUTPUT:
    (1) plot of most common hashtags
    '''
    # read in all tweets as DataFrame
    df = DataFrame_from_tweets(myPath)

    # initialize empty DataFrame to store daily counts
    combinedDF = pd.DataFrame()
    
    for lang in ['ru', 'en']:
        # subset just tweets from one language and save col of hashtags as list
        hashtagList = df.loc[df[kind] == lang].hashtags.tolist()

        realHashtags = []
        for potentialTags in hashtagList:
            tags = ast.literal_eval(potentialTags)
            if tags:
                for tag in tags:
                    realHashtags.append(tag['text'])

        # make FreqDist from a bag of hashtags
        fd = Counter(realHashtags)

        # split words and their counts up for plotting
        words, counts = zip(*fd.most_common(numHashtags))
        indexes = np.arange(len(words))

        # make the plot
        width = 1
        plt.bar(indexes, counts)
        plt.xticks(indexes + width * 0.5, words, rotation=90, fontsize=18)
        plt.tight_layout()
        plt.savefig(lang + "_" + kind + "_" + 'plot.jpg')


def plot_tweet_langs(myPath, numLangs = 10, kind ='tweet_lang'):
    '''
    INPUT:
    (1) a directory of files
    OUTPUT:
    (1) plot of counts of tweets per language
    '''
    # read in all tweets as DataFrame
    df = DataFrame_from_tweets(myPath)

    # count up tweets per language for all languages
    allLangs = Counter(df.loc[:,(kind)])

    # split language codes and their counts up for plotting
    langs, counts = zip(*allLangs.most_common(numLangs))
    indexes = np.arange(len(langs))

    # make the plot
    width = 1
    plt.bar(indexes, counts)
    plt.ylabel("Number of Tweets Per Language")
    plt.xlabel("Language Code")
    plt.xticks(indexes + width * 0.5, langs, rotation=90, fontsize=18)
    plt.tight_layout()
    plt.savefig("tweet_counts_" + kind + "_" + 'plot.jpg')
    print("Your plot has been saved to your working dir.")

    
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


def plot_regex_matches(myPath, searchTerms, kind='tweet_lang'):
    '''
    INPUT:
    (1) a list of unicode search terms
    (2) a directory of files
    (3) either 'user_lang' or 'tweet_lang'
    OUTPUT:
    (1) longitudinal linegraph of percentage of tweets which match given regex
    for each language
    '''
    # read in all tweets as DataFrame
    df = DataFrame_from_tweets(myPath)
    print('tweets read in as Pandas DataFrame...')
    
    # initialize empty DataFrame to store daily counts
    combinedDF = pd.DataFrame()
    
    # compile search terms as one regex
    regex = (u'|').join(searchTerms)

    for lang in ['ru', 'uk', 'en']:
        # subset just tweets from one language
        langDF = df[df.loc[:,(kind)]==lang]
        # convert timestamp to year-month-day format
        langDF.loc[:,('date')] = langDF.loc[:,('time')].apply(lambda x:
                                        pd.to_datetime(x, dayfirst=True).date())
        # lower text of tweets
        langDF.loc[:,('text')] = langDF['text'].apply(lambda x: codecs.decode(x,
                                                            'utf-8').lower())
        # count all tweets in language
        langTotal = langDF.date.value_counts()

        # count tweets containing regex
        langMatches = langDF[langDF.text.str.contains(regex)].date.value_counts()

        # merge the counts into one df, so we can calculate frequency
        freqDF = pd.concat([langMatches, langTotal], axis=1)

        # plus-1 smoothing numerator
        freqDF = freqDF.fillna(1)
        
        # plus-1 smoothing denominator and freq calculation
        freqSeries = freqDF.apply(lambda row: (row[0]/(row[1]+1))*100,
                                        axis=1)
        # add language frequencies to big df
        combinedDF[lang] = freqSeries

        print('one language plotted...')

    combinedDF.plot()
    plt.legend(loc='best')
    plt.title('Political Tweets per Day')
    plt.xlabel("Day")
    plt.ylabel("Percent of Tweets")
    plt.show()
 

def searchTerms():
    politics = u'политик|політик|politic'
    minsk = u'минск.* соглашен|мінськ.* угод|minsk.* agreement'
    putin = u'путин|путін|putin'
    poroshenko = u'порошченко|poroshenko' 
    crimea = u'крым|крим|crimea'
    usa = u'обам. |obama|сша|usa '
    war = u'войн. |війн. |war '
    news = u'новости|новини|news '
    dnr = u'днр|dnr'
    lnr = u'лнр|lnr'
    revolution = u'революци|революці|revolution'
    donbass = u'донбас|donbass'
    donetsk = u'донецк|донецьк|donetsk'
    maidan = u'майдан|maidan'
    sevastopol = u'севастополь|sevastopol'
    merged = [politics, minsk, crimea, usa, war, news, dnr, lnr, revolution,
              donbass, donetsk, sevastopol, putin, poroshenko, maidan]
    return merged
    

def main():

    myPath= sys.argv[1]
    # plot_tweet_langs(myPath, kind="user_lang")
    plot_common_hashtags(myPath, kind="user_lang")

    # terms= searchTerms()
    # plot_length_of_tweets(myPath, kind)
    # plot_regex_matches(myPath, terms)
    
if __name__ == "__main__":
    main()

