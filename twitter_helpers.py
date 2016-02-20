import os
import csv
import pandas as pd

def DataFrame_from_tweets(myPath, extension = '.txt'):
    '''
    INPUT:
    a path to a dir or file
    extension of tweet files (probably .txt or .csv)
    OUTPUT:
    a pandas DataFrame where each row is a tweet
    '''
    # figure out if path is a file or dir
    if os.path.isdir(myPath):
        myDir = myPath
        fileNames = [f for f in os.listdir(myDir) if f.endswith(extension)]
    elif os.path.isfile(myPath):
        myDir = ''
        fileNames = [myPath]

    # make a list of tweets and then convert to pandas DataFrame
    tweets=[]
    for fileName in fileNames:
        print(fileName)
        fullPath = myDir+fileName
        if os.path.isfile(fullPath):
            with open(fullPath, encoding='utf8') as csvfile:
                 f = csv.reader(csvfile, delimiter='\t', quotechar='"')
                 for row in f:
                     tweets.append(row)

            df = pd.DataFrame(tweets, columns=['coords',
                                                 'text',
                                                 'hashtags',
                                                 'time',
                                                 'tweet_lang',
                                                 'user_lang',
                                                 'tweet_id',
                                               'user_id'])
    return df
