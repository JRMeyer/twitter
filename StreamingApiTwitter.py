# Lots of good info about the API at https://dev.twitter.com/overview/api/tweets

import sys
import tweepy
import csv
# Keys are on your application's Details page at https://dev.twitter.com/apps
from accessKeys import consumer_key, consumer_secret, access_key, access_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

class CustomStreamListener(tweepy.StreamListener):
    '''
    This is the listener, resposible for receiving data
    '''
    def __init__(self, api=None):
        self.api = API(retry_count = 10, timeout = 1300)
        
    def on_status(self, tweet):
        # throw out any tweet without geotags
        if tweet.coordinates == None:
            pass
        else:
            tweet_coordinates = \
              (str(tweet.coordinates['coordinates'])).encode('utf-8')

            # replace newline characters with commas in tweet and replace
            # double quotes with singles so we only have exterior doubles
            text = (((tweet.text).replace("\"","'")
                 ).replace("\n", ", ")).encode('utf-8')
            hashtags = (str(tweet.entities['hashtags'])).encode('utf-8')
            timeStamp = (str(tweet.created_at)).encode('utf-8')
            tweetLang = (tweet.lang).encode('utf-8')
            userLang = (tweet.user.lang).encode('utf-8')
            tweetID = (tweet.id_str).encode('utf-8')
            userID = (tweet.user.id_str).encode('utf-8')

            with open(timeStamp.split(' ')[0] +'.txt', 'a') as outFile:
                writer = csv.writer(outFile, delimiter ='\t', quotechar='"')
                writer.writerow([tweet_coordinates, 
                                text,
                                hashtags,
                                timeStamp,
                                tweetLang,
                                userLang,
                                tweetID,
                                 userID])
        return True

    
    def on_error(self, status_code):
        # Don't kill the stream on an error
        return True

    
    def on_timeout(self):
        # Don't kill the stream on timeout
        return True


sapi = tweepy.streaming.Stream(auth, CustomStreamListener())

# to get all geotagged tweets in world, use [-180,-90,180,90]
sapi.filter(locations=[22.1357201, # Western longitude
                       44.386383,  # Southern latitude
                       40.227172,  # Eastern longitude
                       52.379475]) # Northern latitude
